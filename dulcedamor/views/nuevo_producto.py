from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Producto, Categoria

def nuevo_producto(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías disponibles

    if request.method == 'POST':
        # Obtener los datos del formulario
        codigo = request.POST['codigo']
        nombre = request.POST['producto']
        precio = request.POST['precio']
        stock = request.POST['stock']
        estado = request.POST['estado']
        categoria_id = request.POST['categoria']  # Obtenemos el id de la categoría seleccionada
        
        # Verificar que la categoría seleccionada es válida
        try:
            categoria = Categoria.objects.get(id=categoria_id)  # Obtener el objeto Categoria por su id
        except Categoria.DoesNotExist:
            messages.error(request, "La categoría seleccionada no es válida.")
            return redirect('nuevo_producto')  # Redirigir si no existe la categoría

        # Crear un nuevo producto
        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            stock=stock,
            estado=estado,
            nombre_categoria=categoria  # Relacionamos la categoría seleccionada con el producto
        )
        producto.save()

        messages.success(request, "Producto creado exitosamente.")
        return redirect('productos')  # Redirigir a la lista de productos

    return render(request, 'nuevo_producto.html', {'categorias': categorias})
