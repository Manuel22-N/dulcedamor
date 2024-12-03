from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import CustomUser, Role
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='user_login')
@csrf_exempt
def gestionar_usuarios(request):
    # Recuperar usuarios y roles
    usuarios = CustomUser.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':
        # Crear un nuevo usuario
        if 'crear_usuario' in request.POST:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            correo = request.POST.get('correo')
            celular = request.POST.get('celular')
            rol_id = request.POST.get('rol')
            password = request.POST.get('password')

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
