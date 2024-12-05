from django.shortcuts import render, get_object_or_404, redirect
from users.models import Categoria

def editar_categorias(request):
    if request.method == 'POST':
        # Obtener el código de la categoría desde el formulario
        codigo_categoria = request.POST.get('codigoCategoria')

        # Buscar la categoría con ese código
        categoria = get_object_or_404(Categoria, codigo=codigo_categoria)

        # Obtener los datos del formulario para el nombre y estado
        nombre_categoria = request.POST.get('nombreCategoria')
        estado_categoria = request.POST.get('estado')

        # Actualizar los valores de la categoría
        categoria.nombre = nombre_categoria
        categoria.estado = estado_categoria
        categoria.save()

        # Redirigir después de la actualización
        return redirect('categorias')  # Cambia esto según la vista que desees

    # Si no es un POST, mostrar la página para editar
    return render(request, 'editar_categorias.html')
