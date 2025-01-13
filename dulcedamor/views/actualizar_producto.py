from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from users.models import Producto

def actualizar_producto(request, id):  
    # Buscar el producto por su ID
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        # Obtener los valores de los campos del formulario
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        estado = request.POST.get('estado')
        imagen = request.FILES.get('imagen')
        
        

        # Actualizar los campos solo si se proporcionan valores
        if nombre:
            producto.nombre = nombre
        if codigo:
            producto.codigo = codigo
        if precio:
            producto.precio = precio
        if stock:
            producto.stock = stock
        if estado:
            producto.estado = estado
        
        # Si se ha subido una nueva imagen, actualizar el campo 'imagen'
        if imagen:
            producto.imagen = imagen
        
        # Guardar los cambios en la base de datos
        producto.save()

        # Mensaje de éxito y redirección a la lista de productos
        messages.success(request, "Producto actualizado con éxito.")
        return redirect('productos')  # Redirige a la lista de productos

    # Si es un GET, mostrar el formulario de actualización
    return render(request, 'actualizar_producto.html', {'producto': producto})
