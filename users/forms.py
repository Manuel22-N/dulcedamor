from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """
        Devuelve usuarios activos que coincidan con el email dado.
        """
        UserModel = get_user_model()  # Obtiene el modelo configurado en AUTH_USER_MODEL
        return UserModel.objects.filter(email=email, is_active=True)
