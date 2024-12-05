from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Categoria
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def nueva_categoria(request):
    if request.method == 'POST':
        # Recuperar los datos del formulario
        codigo = request.POST.get('codigo')  # Campo "codigo"
        nombre_categoria = request.POST.get('nombre')  # Campo "nombre"
        estado = request.POST.get('estado')  # Campo "estado"

        # Validación: asegurarse de que 'codigo' no sea vacío
        if not codigo:
            messages.error(request, 'El código de la categoría es obligatorio.')
            return redirect('nueva_categoria')

        # Validación para el estado
        if estado not in ['activo', 'inactivo']:
            messages.error(request, 'El estado debe ser "activo" o "inactivo".')
            return redirect('nueva_categoria')

        try:
            # Crear la nueva categoría
            nueva_categoria = Categoria(
                codigo=codigo,
                nombre=nombre_categoria,
                estado=estado,
            )
            nueva_categoria.save()
            messages.success(request, 'Categoría registrada con éxito.')
        except Exception as e:
            messages.error(request, 'No se pudo crear la categoría. Intenta de nuevo.')

        # Redirigir a la misma vista para limpiar el formulario y mostrar los mensajes
        return redirect('categorias')

    return render(request, 'nueva_categoria.html')