from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from users.models import CustomUser, Role
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required(login_url='user_login')
@csrf_exempt
def gestionar_usuarios(request):
    # Recuperar usuarios y roles
    usuarios = CustomUser.objects.all()
    roles = Role.objects.all()

     # Verifica si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        search_query = request.GET.get('search', '')
        usuarios = usuarios.filter(
            first_name__icontains=search_query
        ) | usuarios.filter(
            last_name__icontains=search_query
        ) | usuarios.filter(
            email__icontains=search_query
        )
        usuarios_data = [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone if user.phone else 'No registrado',  
                'role': user.role.name if user.role else 'Sin rol', 
                'is_active': user.is_active
            }
            for user in usuarios
        ]
        return JsonResponse({'usuarios': usuarios_data})

    if request.method == 'POST':
        # Crear un nuevo usuario
        if 'crear_usuario' in request.POST:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            correo = request.POST.get('correo')
            celular = request.POST.get('celular')
            rol_id = request.POST.get('rol')
            password = request.POST.get('password')

             # Validar si el correo ya existe
            if CustomUser.objects.filter(email=correo).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
                return redirect('gestionar_usuarios')

            # Validar rol
            try:
                rol = Role.objects.get(id=rol_id)
            except Role.DoesNotExist:
                messages.error(request, 'Rol seleccionado no es válido.')
                return redirect('gestionar_usuarios')

            # Crear usuario con contraseña hasheada
            nuevo_usuario = CustomUser(
                first_name=nombre,
                last_name=apellido,
                email=correo,
                phone=celular,
                role=rol,
            )
            nuevo_usuario.set_password(password)
            nuevo_usuario.save()
            messages.success(request, 'Usuario registrado con éxito.')

        # Eliminar un usuario
        elif 'eliminar_usuario' in request.POST:
            usuario_id = request.POST.get('usuario_id')
            usuario = get_object_or_404(CustomUser, id=usuario_id)

            # Prevenir la eliminación de la cuenta activa
            if usuario == request.user:
                messages.error(request, 'No puedes eliminar tu propia cuenta.')
                return redirect('gestionar_usuarios')

            usuario.delete()
            messages.success(request, 'Usuario eliminado con éxito.')

        # Activar o desactivar un usuario
        elif 'cambiar_estado' in request.POST:
            usuario_id = request.POST.get('usuario_id')
            usuario = get_object_or_404(CustomUser, id=usuario_id)

            # Prevenir desactivación de la cuenta activa
            if usuario == request.user:
                messages.error(request, 'No puedes desactivar tu propia cuenta.')
                return redirect('gestionar_usuarios')

            usuario.is_active = not usuario.is_active  # Cambiar el estado
            usuario.save()
            messages.success(request, f"Usuario {'activado' if usuario.is_active else 'desactivado'} con éxito.")

    # Renderizar la plantilla
    return render(request, 'gestionar_usuarios.html', {
        'usuarios': usuarios,  
        'roles': roles,
    })

@login_required(login_url='user_login')
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)
    roles = Role.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        celular = request.POST.get('celular')
        rol_id = request.POST.get('rol')

        # Validar si el correo ya está registrado por otro usuario
        if CustomUser.objects.filter(email=correo).exclude(id=usuario.id).exists():
            messages.error(request, 'El correo electrónico ya está en uso por otro usuario.')
            return redirect('editar_usuario', usuario_id=usuario.id)

        # Validar rol
        try:
            rol = Role.objects.get(id=rol_id)
        except Role.DoesNotExist:
            messages.error(request, 'Rol seleccionado no es válido.')
            return redirect('editar_usuario', usuario_id=usuario.id)

        # Actualizar los datos del usuario
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.phone = celular
        usuario.role = rol
        usuario.save()

        messages.success(request, 'Usuario actualizado con éxito.')
        return redirect('gestionar_usuarios')

    return render(request, 'editar_usuario.html', {'usuario': usuario, 'roles': roles})
