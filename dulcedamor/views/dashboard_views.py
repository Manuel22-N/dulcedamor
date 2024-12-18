from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model  # Obtener el modelo de usuario actual
from users.models import Categoria,Producto

@login_required(login_url='user_login')  # Redirige al login si no está autenticado
def dashboard_view(request):
    # Obtener el modelo de usuario
    User = get_user_model()
    # Contar los usuarios registrados
    user_count = User.objects.count()

    category_count = Categoria.objects.count()  # Esto cuenta las categorías
    product_count = Producto.objects.count()
    
    # Pasar el conteo al contexto de la plantilla
    context = {
        'user_count': user_count,
        'category_count': category_count,
        'product_count':product_count
    }
    return render(request, 'dashboard.html', context)
