from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import Categoria
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='user_login')
def categorias(request):
    categorias = Categoria.objects.all()  # Obtiene todas las categorías desde la base de datos
    return render(request, 'categorias.html', {'categorias': categorias})


@csrf_exempt
def nueva_categorias(request):
    # Recuperar categorías
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        # Si el formulario es para crear una nueva categoría
        if 'crear_categoria' in request.POST:
            codigo = request.POST.get('codigo')
            nombre_categoria = request.POST.get('nombre de categoria')
            estado = request.POST.get('Estado')

            # Validación simple para el estado
            if estado not in ['activo', 'inactivo']:
                # Mensaje de error si el estado no es válido
                return redirect('categorias')

            # Crear la nueva categoría
            nueva_categoria = Categoria(
                codigo=codigo,
                nombre=nombre_categoria,
                estado=estado,
            )
            nueva_categoria.save()
            # Aquí eliminamos el mensaje de éxito de categoría registrada

        # Si el formulario es para eliminar una categoría
        elif 'eliminar_categoria' in request.POST:
            categoria_id = request.POST.get('categoria_id')
            categoria = get_object_or_404(Categoria, id=categoria_id)
            categoria.delete()
            # Aquí eliminamos el mensaje de éxito de categoría eliminada

    return render(request, 'categorias.html', {'categorias': categorias})


@login_required(login_url='user_login')
def categorias(request):
    categorias = Categoria.objects.all()  # Obtiene todas las categorías desde la base de datos

    if request.method == 'POST' and 'eliminar_categoria' in request.POST:
        categoria_id = request.POST.get('categoria_id')  # Obtén el ID de la categoría a eliminar
        categoria = get_object_or_404(Categoria, id=categoria_id)  # Recupera la categoría

        # Elimina la categoría, pero no mostramos el mensaje de éxito
        categoria.delete()

        return redirect('categorias')  # Redirige a la misma página después de la eliminación

    return render(request, 'categorias.html', {'categorias': categorias})


@csrf_exempt
def nueva_categoria(request):
    if request.method == 'POST':
        # Si el formulario es para crear una nueva categoría
        if 'crear_categoria' in request.POST:
            codigo = request.POST.get('dni')  # El campo 'dni' en el formulario
            nombre_categoria = request.POST.get('nombre')
            estado = request.POST.get('estado')

            # Validación simple para el estado
            if estado not in ['activo', 'inactivo']:
                # Mensaje de error si el estado no es válido
                return redirect('nueva_categoria')

            # Crear la nueva categoría
            nueva_categoria = Categoria(
                codigo=codigo,
                nombre=nombre_categoria,
                estado=estado,
            )
            nueva_categoria.save()
            # Aquí eliminamos el mensaje de éxito de categoría registrada

            # Redirigir después de guardar
            return redirect('categoria')  # O redirigir a donde desees

    return render(request, 'nueva_categoria.html')








