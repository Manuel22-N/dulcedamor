from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views  # Importamos las vistas personalizadas de la app users
from .forms import CustomPasswordResetForm  # Importamos el formulario personalizado
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView  # Vistas personalizadas

urlpatterns = [
    # Ruta para el login
    path('login/', views.user_login, name='user_login'),

    # Ruta para el logout
    path('logout/', LogoutView.as_view(next_page='user_login'), name='user_logout'),

    # Restablecimiento de contraseña
    path(
        'password-reset/',
        CustomPasswordResetView.as_view(
            template_name='password_reset_form.html',  # Tu plantilla personalizada
            form_class=CustomPasswordResetForm,       # Usar el formulario personalizado
        ),
        name='password_reset_request'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        CustomPasswordResetConfirmView.as_view(
            template_name='password_reset_email.html',  
        ),
        name='password_reset_confirm'
    ),
]
