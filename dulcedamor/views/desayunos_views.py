import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import Producto
from django.db import transaction

# Vista para renderizar la página de desayunos
@login_required(login_url='user_login')
def desayunos(request):
    return render(request, 'desayunos.html')

# --- Función para buscar producto por código ---
@login_required(login_url='user_login')
def buscar_producto(request, codigo):
    try:
        producto = Producto.objects.get(codigo=codigo, estado="activo")
        return JsonResponse({"success": True, "nombre": producto.nombre})
    except Producto.DoesNotExist:
        return JsonResponse({"success": False, "error": "Producto no encontrado"})

# --- Función para guardar los productos y descontar stock ---
@login_required(login_url='user_login')
@transaction.atomic
def guardar_desayuno(request):
    if request.method == "POST":
        try:
            productos = json.loads(request.body).get('productos', [])
            if not productos:
                return JsonResponse({"success": False, "mensaje": "No se han agregado productos en ninguna tabla."})

            # Validar stock de todos los productos antes de descontar
            productos_insuficientes = []
            for item in productos:
                codigo = item.get("codigo")
                cantidad = item.get("cantidad")

                try:
                    producto = Producto.objects.get(codigo=codigo, estado="activo")
                    if producto.stock < cantidad:
                        productos_insuficientes.append(f"{codigo} (stock disponible: {producto.stock}, solicitado: {cantidad})")
                except Producto.DoesNotExist:
                    productos_insuficientes.append(f"{codigo} (no existe)")

            # Si hay productos con problemas, abortar la operación
            if productos_insuficientes:
                mensaje_error = "No se pudo realizar la operación. Los siguientes productos tienen problemas: " + ", ".join(productos_insuficientes)
                return JsonResponse({"success": False, "mensaje": mensaje_error})

            # Realizar el descuento si todo está en orden
            for item in productos:
                codigo = item.get("codigo")
                cantidad = item.get("cantidad")
                producto = Producto.objects.get(codigo=codigo, estado="activo")
                producto.stock -= cantidad
                producto.save()

            return JsonResponse({"success": True, "mensaje": "Operación exitosa. Los productos fueron descontados del inventario."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "mensaje": "Datos mal formateados."})
    
    return JsonResponse({"success": False, "mensaje": "Método no permitido."})