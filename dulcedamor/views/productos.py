from django.shortcuts import render, redirect
from users.models import Producto  # Asumiendo que el modelo Producto está en users.models
from django.db.models import Q  # Importar Q para realizar búsquedas complejas
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator  # Importar Paginator para la paginación

@login_required(login_url='user_login')
def productos(request):
    # Obtener el valor de búsqueda desde el parámetro GET
    query = request.GET.get('search', '')  # Obtén el parámetro de búsqueda
    
    # Filtrar los productos si hay un valor en la búsqueda
    productos = Producto.objects.all()

    if query:
        productos = productos.filter(
            Q(codigo__icontains=query) | Q(nombre__icontains=query)
        )
    
    mensaje = None  # Definir un valor por defecto para 'mensaje'

    if request.method == 'POST':
        if 'eliminar_producto' in request.POST:
            producto_id = request.POST.get('producto')
            try:
                producto = Producto.objects.get(id=producto_id)
                producto.delete()  # Eliminar el producto
                mensaje = "Producto eliminado correctamente"  # Mensaje de éxito
            except Producto.DoesNotExist:
                mensaje = "El producto no existe"  # Mensaje de error si el producto no existe

            return redirect('productos')  # Redirigir a la misma página después de eliminar
    
    # Paginación
    paginator = Paginator(productos, 10)  # 10 productos por página
    page = request.GET.get('page')  # Obtener la página actual desde los parámetros GET
    productos_paginados = paginator.get_page(page)

    return render(request, 'productos.html', {'productos': productos_paginados, 'mensaje': mensaje, 'query': query})
