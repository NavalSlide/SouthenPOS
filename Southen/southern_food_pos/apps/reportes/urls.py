from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    # Vista principal de reportes
    path('', views.reportes_view, name='index'),
    
    # Reportes Financieros y Fiscales
    path('ventas/', views.ventas_report, name='ventas'),
    path('iva/', views.iva_report, name='iva'),
    path('facturas/', views.facturas_report, name='facturas'),
    
    # Reportes Operativos
    path('inventario/', views.inventario_report, name='inventario'),
    path('analisis-ventas/', views.analisis_ventas_report, name='analisis_ventas'),
    path('clientes/', views.clientes_report, name='clientes'),
    
    # Reportes para el SRI
    path('ats/', views.ats_report, name='ats'),
    path('iva-declaracion/', views.iva_declaracion_report, name='iva_declaracion'),
    path('renta/', views.renta_report, name='renta'),
    
    # Reportes Rápidos
    path('ventas-diarias/', views.ventas_diarias_report, name='ventas_diarias'),
    path('productos-top/', views.productos_top_report, name='productos_top'),
    path('stock-bajo/', views.stock_bajo_report, name='stock_bajo'),
    path('generar-xml/', views.generar_xml, name='generar_xml'),
]