from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import Salida


def salidas(request):
    """
    Vista para listar todas las salidas.
    """
    salidas = Salida.objects.all()  # Obtén todas las salidas
    return render(request, 'salidas.html', {'salidas': salidas})


def eliminar_salida(request, salida_id):
    """
    Vista para eliminar un registro de salida específico.
    """
    if request.method == 'POST':
        salida = get_object_or_404(Salida, id=salida_id)
        salida.delete()
        messages.success(request, "La salida fue eliminada correctamente.")
        return redirect('salidas')


def eliminar_por_rango(request):
    """
    Vista para eliminar salidas dentro de un rango de fechas.
    """
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Verifica que ambas fechas sean válidas
        if fecha_inicio and fecha_fin:
            Salida.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).delete()
            messages.success(request, "Se eliminaron las salidas dentro del rango de fechas.")
        else:
            messages.error(request, "Por favor, proporciona un rango de fechas válido.")
        return redirect('salidas')
