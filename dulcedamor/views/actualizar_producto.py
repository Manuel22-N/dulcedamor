from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Producto

@login_required(login_url='user_login')
def actualizar_producto(request, id):  # Asegúrate de que 'id' se pasa como argumento
    # Buscar el producto por su ID
    producto = get_object_or_404(Producto, id=id)

    # Si se envía un formulario de actualización de producto
    if request.method == 'POST':
        # Actualizar los campos del producto
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')
        producto.estado = request.POST.get('estado')

        # Guardar los cambios
        producto.save()

        # Mensaje de éxito y redirección a la lista de productos
        messages.success(request, "Producto actualizado con éxito.")
        return redirect('productos')  # Redirige a la lista de productos

    # Si es un GET, simplemente mostrar el formulario de actualización
    return render(request, 'actualizar_producto.html', {'producto': producto})
