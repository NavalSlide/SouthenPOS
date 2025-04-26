from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.lista_clientes, name='lista'),
    path('agregar/', views.agregar_cliente, name='agregar'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar'),
    path('eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar'),
    path('detalle/<int:cliente_id>/', views.detalle_cliente, name='detalle'),
    # Change this to a different path
    path('search/', views.client_search_view, name='client_search'),
]
