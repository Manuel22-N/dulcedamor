from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from users.models import Producto

def actualizar_producto(request):
    # Si el formulario de búsqueda se envía
    if request.method == 'POST' and 'codigo' in request.POST:
        codigo_producto = request.POST['codigo']
        try:
            # Buscar el producto por código
            producto = Producto.objects.get(codigo=codigo_producto)
            return render(request, 'actualizar_producto.html', {'producto': producto})
        except Producto.DoesNotExist:
            # Si no se encuentra el producto, mostramos un mensaje de error
            messages.error(request, "Producto no encontrado con ese código.")
            return redirect('actualizar_producto')  # Redirige a la misma página si no se encuentra el producto

    # Si el formulario de actualización de producto se envía
    elif request.method == 'POST' and 'producto_id' in request.POST:
        producto_id = request.POST['producto_id']
        producto = get_object_or_404(Producto, id=producto_id)

        # Actualizamos los campos del producto
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.estado = request.POST['estado']

        # Guardamos el producto actualizado
        producto.save()

        # Mensaje de éxito y redirección a la lista de productos (o dashboard)
        messages.success(request, "Producto actualizado con éxito.")
        return redirect('productos')  # Redirige a la lista de productos (o dashboard)

    # Si no es un POST, simplemente mostramos la página vacía
    return render(request, 'actualizar_producto.html')






