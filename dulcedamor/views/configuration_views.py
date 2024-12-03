from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from dulcedamor.forms.forms import CustomPasswordChangeForm
from django.contrib.auth.models import User

@login_required(login_url='user_login')  # Aseguramos que solo los usuarios autenticados puedan acceder
def configuration_view(request):
    form = CustomPasswordChangeForm(user=request.user)  # Definimos la variable form antes de entrar al bloque POST

    if request.method == 'POST':
        if 'first_name' in request.POST and 'last_name' in request.POST:
            # Procesar los datos del formulario de edición
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            # Actualizar la información del usuario
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone = phone  # Asegúrate de tener el campo 'phone' en el modelo de usuario
            user.save()

            messages.success(request, 'Información actualizada con éxito.')
            return redirect('configuration')  # Redirige para evitar reenvío del formulario
        else:
            # Usar el formulario personalizado para cambiar la contraseña
            form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Mantener al usuario logueado después del cambio de contraseña
                messages.success(request, 'La contraseña se ha cambiado con éxito.')
                return redirect('configuration')  # Redirige de nuevo a la página de configuración

    # Retornar la plantilla con la información del usuario y el formulario para cambiar la contraseña
    return render(request, 'configuration.html', {
        'form': form,
        'user': request.user,
    })
