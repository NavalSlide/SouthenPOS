from django.urls import path
from . import views

app_name = 'productos'  # This is crucial for the namespace

urlpatterns = [
    path('', views.lista_productos, name='lista'),  # This is the correct name
    path('nuevo/', views.crear_producto, name='crear'),
    path('editar/<int:pk>/', views.editar_producto, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar'),
    # Add this new category route
    path('categorias/nueva/', views.crear_categoria, name='categoria_create'),
    # Add this to your existing URL patterns
    path('buscar/', views.buscar_productos, name='buscar'),
]