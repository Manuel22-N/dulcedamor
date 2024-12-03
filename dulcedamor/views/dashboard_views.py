from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model  # Obtener el modelo de usuario actual

@login_required(login_url='user_login')  # Redirige al login si no está autenticado
def dashboard_view(request):
    # Obtener el modelo de usuario
    User = get_user_model()
    # Contar los usuarios registrados
    user_count = User.objects.count()
    
    # Pasar el conteo al contexto de la plantilla
    context = {
        'user_count': user_count,
    }
    return render(request, 'dashboard.html', context)
