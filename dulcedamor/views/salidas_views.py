from django.shortcuts import render
from users.models import Salida

def salidas(request):
    # Filtramos las salidas, asumiendo que todas son de la categoría desayuno
    salidas = Salida.objects.all()  # Aquí puedes filtrar por una categoría específica si es necesario
    return render(request, 'salidas.html', {'salidas': salidas})
