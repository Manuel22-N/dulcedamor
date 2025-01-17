from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model  # Importamos get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetConfirmView
from .forms import CustomPasswordResetForm

# Vista para el login
def user_login(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST['username']
        password = request.POST['password']

        # Validar las credenciales
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Obtener el rol del usuario desde la relación de clave foránea
            user_role = user.role.name.lower() if user.role else None  # Convertir a minúsculas por consistencia

            # Redirigir al dashboard si es administrador
            if request.user.role.name == 'Administrador' or request.user.role.name == 'Auxiliar':
                return redirect('dashboard')  # Redirigir al dashboard

           

            # Si no tiene un rol válido, mostrar un mensaje de error
            else:
                messages.error(request, 'No tienes un rol asignado válido.')
                return redirect('user_login')

        else:
            messages.error(request, 'Credenciales incorrectas. Intenta de nuevo.')

    # Si no es un POST, o si las credenciales son incorrectas, se vuelve a mostrar el formulario de login
    return render(request, 'login.html')


# Vista para el restablecimiento de la contraseña
class CustomPasswordResetView(SuccessMessageMixin, FormView):
    template_name = 'password_reset_form.html'  # Usamos esta plantilla para solicitar el correo
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_request')
    success_message = (
        "Si existe una cuenta asociada con este correo, "
        "se enviará un enlace para restablecer la contraseña."
    )

    def form_valid(self, form):
        # Obtener el correo electrónico
        email = form.cleaned_data.get('email')
        UserModel = get_user_model()  # Obtener el modelo configurado en AUTH_USER_MODEL
        try:
            user = UserModel.objects.get(email=email)  # Usar el modelo personalizado
        except UserModel.DoesNotExist:
            # No revelar si el usuario existe por seguridad
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)

        # Generar token y enlace
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = self.request.build_absolute_uri(reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

        # Enviar correo
        subject = 'Restablecimiento de contraseña'
        message = render_to_string('template_reset_password.html', {
            'user': user,
            'reset_url': reset_url,
        })
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        except Exception:
            messages.error(self.request, 'Ocurrió un problema al enviar el correo. Intenta de nuevo más tarde.')
            return redirect(self.success_url)

        # Mostrar mensaje de éxito
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)


# Vista para el formulario de confirmación de contraseña
class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'  # Aquí usamos la plantilla donde se ingresan las nuevas contraseñas
    success_url = reverse_lazy('user_login')
    success_message = "Tu contraseña ha sido restablecida exitosamente. Ahora puedes iniciar sesión."

    def form_valid(self, form):
        return super().form_valid(form)
