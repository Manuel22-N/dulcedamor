from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from users.models import Categoria

@login_required(login_url='user_login')
def editar_categorias(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        # Obtener los valores del formulario
        nombre_categoria = request.POST.get('nombre')  # Asegúrate de usar 'nombre' aquí
        estado_categoria = request.POST.get('estado')

        # Verificar que el campo 'nombre' no esté vacío
        if not nombre_categoria:
            return render(request, 'editar_categorias.html', {
                'categoria': categoria,
                'error': 'El nombre de la categoría es obligatorio.'
            })

        # Actualizar los valores de la categoría
        categoria.nombre = nombre_categoria
        categoria.estado = estado_categoria
        categoria.save()

        # Redirigir después de la actualización
        return redirect('categorias')

    return render(request, 'editar_categorias.html', {'categoria': categoria})
