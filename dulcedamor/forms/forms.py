from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].error_messages['password_too_short'] = _(
            "La contraseña es demasiado corta. Debe contener al menos 8 caracteres."
        )

    class Meta:
        model = CustomUser
        fields = ('password',)

    error_messages = {
        'password_incorrect': _("Tu contraseña actual es incorrecta. Por favor, inténtalo de nuevo."),
        'password_mismatch': _("Las contraseñas no coinciden. Por favor, inténtalo de nuevo."),
        'password_too_short': _("La contraseña es demasiado corta. Debe contener al menos 8 caracteres."),
        'password_common': _("Esta contraseña es demasiado común. Elige una contraseña más segura."),
        'password_similar': _("La contraseña es demasiado similar al nombre de usuario. Elige otra."),
    }
