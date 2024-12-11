from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Categoria
from django.db.models import Q  # Importar Q para realizar búsquedas complejas
from django.utils.translation import activate
from django.core.paginator import Paginator  # Importar Paginator

@login_required(login_url='user_login')
def categorias(request):
    activate('es')
    
    # Obtener el valor de búsqueda desde el parámetro GET
    query = request.GET.get('search', '')  # Obtén el parámetro de búsqueda
    
    # Obtener el valor de 'tbl_length' para saber cuántos elementos mostrar por página
    tbl_length = int(request.GET.get('tbl_length', 10))  # Valor por defecto es 10
    
    # Filtrar las categorías si hay un valor en la búsqueda
    categorias = Categoria.objects.all()

    if query:
        categorias = categorias.filter(
            Q(codigo__icontains=query) | Q(nombre__icontains=query)
        )

    # Paginación
    paginator = Paginator(categorias, tbl_length)  # Paginación según el valor de 'tbl_length'
    page = request.GET.get('page')  # Obtener la página actual desde los parámetros GET
    categorias_paginadas = paginator.get_page(page)  # Obtener las categorías para la página actual

    # Procesar solicitudes POST (eliminar o crear categoría)
    if request.method == 'POST':
        if 'eliminar_categoria' in request.POST:
            # Eliminar categoría
            categoria_id = request.POST.get('categoria_id')  # Obtén el ID de la categoría a eliminar
            categoria = get_object_or_404(Categoria, id=categoria_id)  # Recupera la categoría
            categoria.delete()  # Elimina la categoría
            messages.success(request, 'Categoría eliminada con éxito.')
        
        elif 'crear_categoria' in request.POST:
            # Crear nueva categoría
            codigo = request.POST.get('codigo')  # Campo "codigo"
            nombre_categoria = request.POST.get('nombre')  # Campo "nombre"
            estado = request.POST.get('estado')  # Campo "estado"

            # Validación: asegurarse de que 'codigo' no sea vacío
            if not codigo:
                messages.error(request, 'El código de la categoría es obligatorio.')
                return redirect('categorias')  # Redirigir para mantener los mensajes

            # Validación para el estado
            if estado not in ['activo', 'inactivo']:
                messages.error(request, 'El estado debe ser "activo" o "inactivo".')
                return redirect('categorias')  # Redirigir para mantener los mensajes

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

        # Redirigir para evitar resubir el formulario si se recarga la página
        return redirect('categorias')

    # Si la solicitud es GET, simplemente se muestra la página con las categorías existentes
    return render(request, 'categorias.html', {
        'categorias': categorias_paginadas,
        'query': query,
        'tbl_length': tbl_length  # Pasar el valor de 'tbl_length' a la plantilla
    })
