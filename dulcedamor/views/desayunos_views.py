import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import Producto,Salida
from django.db import transaction
from users.models import Producto, Salida, Categoria
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas





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

            # Realizar el descuento y registrar las salidas
            for item in productos:
                codigo = item.get("codigo")
                cantidad = item.get("cantidad")
                producto = Producto.objects.get(codigo=codigo, estado="activo")
                producto.stock -= cantidad
                producto.save()

                # Obtener la categoría del producto
                categoria_nombre = producto.nombre_categoria.nombre

                # Registrar la salida en el modelo Salida
                salida = Salida.objects.create(
                    producto=producto,
                    cantidad=cantidad,
                    fecha=item.get("fecha"),  # Asume que 'fecha' viene en el item
                    usuario=request.user,  # El usuario logueado
                    precio=producto.precio * cantidad,  # El precio por cantidad
                    categoria=categoria_nombre  # Almacenar la categoría en la salida
                )
            
            return JsonResponse({"success": True, "mensaje": "Operación exitosa. Los productos fueron descontados y registrados en las salidas."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "mensaje": "Datos mal formateados."})
    
    return JsonResponse({"success": False, "mensaje": "Método no permitido."})


@login_required(login_url='user_login')


def generar_reporte(request):
    # Obtener las fechas del query string
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Convertir las fechas a objetos datetime
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d') if fecha_inicio_str else None
    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d') if fecha_fin_str else None

    # Filtrar las salidas según el rango de fechas
    salidas = Salida.objects.all()
    if fecha_inicio:
        salidas = salidas.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        salidas = salidas.filter(fecha__lte=fecha_fin)

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_salidas.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    # Agregar título y cabecera
    pdf.drawString(100, 750, "Reporte de Salidas de Productos")
    pdf.drawString(100, 730, f"Desde: {fecha_inicio_str} Hasta: {fecha_fin_str}")
    
    # Agregar encabezado de la tabla
    y_position = 700
    pdf.drawString(25, y_position, "#")
    pdf.drawString(50, y_position, "Producto")
    pdf.drawString(125, y_position, "Cantidad")
    pdf.drawString(200, y_position, "Fecha")
    pdf.drawString(300, y_position, "Categoría")
    pdf.drawString(400, y_position, "Usuario")
    pdf.drawString(500, y_position, "Precio")

    # Agregar datos de las salidas
    y_position -= 20
    for i, salida in enumerate(salidas, 1):
        pdf.drawString(25, y_position, str(i))
        pdf.drawString(50, y_position, salida.producto)
        pdf.drawString(125, y_position, str(salida.cantidad))
        pdf.drawString(200, y_position, salida.fecha.strftime("%d/%m/%Y %H:%M"))
        pdf.drawString(300, y_position, salida.categoria)
        pdf.drawString(400, y_position, f"{salida.usuario.first_name} {salida.usuario.last_name}")
        pdf.drawString(500, y_position, str(salida.precio))
        y_position -= 20

    pdf.showPage()
    pdf.save()

    return response
