# views.py
from django.shortcuts import render, redirect
from users.models import Producto  # Asumiendo que el modelo Producto está en users.models

def productos(request):
    productos = Producto.objects.select_related('nombre_categoria').all()  # Seleccionamos la relación
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

    return render(request, 'productos.html', {'productos': productos, 'mensaje': mensaje})






