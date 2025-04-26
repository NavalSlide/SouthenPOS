from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.productos.models import Producto, Categoria
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField, FloatField
from django.db.models.functions import Coalesce

@login_required
def reportes_view(request):
    """Vista principal del panel de reportes"""
    return render(request, 'reportes/reportes.html')

# Reportes Financieros y Fiscales
@login_required
def ventas_report(request):
    """Reporte de ventas diarias, semanales, mensuales y anuales"""
    return render(request, 'reportes/ventas.html')

@login_required
def iva_report(request):
    """Reporte de IVA"""
    return render(request, 'reportes/iva.html')

@login_required
def facturas_report(request):
    """Reporte de facturas y comprobantes"""
    return render(request, 'reportes/facturas.html')

# Reportes Operativos
@login_required
def inventario_report(request):
    """Reporte de inventario"""
    # Obtener solo los productos del usuario actual ordenados por stock
    productos = Producto.objects.filter(usuario_creador=request.user).order_by('stock')
    
    # Productos con stock bajo (menos de 10 unidades)
    productos_stock_bajo = productos.filter(stock__lt=10)
    
    # Productos agotados
    productos_agotados = productos.filter(stock=0)
    
    # Productos por categoría - Solo categorías con productos del usuario
    categorias = Categoria.objects.filter(producto__usuario_creador=request.user).distinct().annotate(
        total_productos=Count('producto', filter=F('producto__usuario_creador') == request.user)
    )
    
    # Calculate valor_inventario separately for each category
    for categoria in categorias:
        productos_categoria = Producto.objects.filter(categoria=categoria, usuario_creador=request.user)
        valor_inventario = sum(p.precio * p.stock for p in productos_categoria)
        categoria.valor_inventario = valor_inventario
    
    # Valor total del inventario - Calculate directly
    valor_total = sum(p.precio * p.stock for p in productos)
    
    context = {
        'productos': productos,
        'productos_stock_bajo': productos_stock_bajo,
        'productos_agotados': productos_agotados,
        'categorias': categorias,
        'valor_total': valor_total,
        'total_productos': productos.count(),
        'total_categorias': categorias.count(),
    }
    
    return render(request, 'reportes/inventario.html', context)

@login_required
def analisis_ventas_report(request):
    """Análisis de ventas"""
    return render(request, 'reportes/analisis_ventas.html')

@login_required
def clientes_report(request):
    """Reporte de clientes"""
    return render(request, 'reportes/clientes.html')

# Reportes para el SRI
@login_required
def ats_report(request):
    """Anexo Transaccional Simplificado (ATS)"""
    return render(request, 'reportes/ats.html')

@login_required
def iva_declaracion_report(request):
    """Declaración del IVA (Formulario 104)"""
    return render(request, 'reportes/iva_declaracion.html')

@login_required
def renta_report(request):
    """Declaración del Impuesto a la Renta"""
    return render(request, 'reportes/renta.html')

# Reportes Rápidos
@login_required
def ventas_diarias_report(request):
    """Reporte de ventas del día"""
    return render(request, 'reportes/ventas_diarias.html')

@login_required
def productos_top_report(request):
    """Reporte de productos más vendidos"""
    return render(request, 'reportes/productos_top.html')

@login_required
def stock_bajo_report(request):
    """Reporte de productos con stock bajo"""
    return render(request, 'reportes/stock_bajo.html')

@login_required
def generar_xml(request):
    """Generación de archivos XML para el SRI"""
    return render(request, 'reportes/generar_xml.html')