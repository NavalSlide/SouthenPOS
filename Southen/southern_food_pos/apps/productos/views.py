from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm
from django.views.generic import CreateView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            # Associate the category with the current user
            categoria.usuario_creador = request.user
            categoria.save()
            return redirect('productos:lista')
    else:
        form = CategoriaForm()
    
    return render(request, 'productos/categoria_form.html', {'form': form})

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'productos/categoria_form.html'
    
    def form_valid(self, form):
        # Associate the category with the current user
        form.instance.usuario_creador = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('productos:lista')

@login_required
def lista_productos(request):
    # Filter products to show only those created by the current user
    productos = Producto.objects.filter(
        usuario_creador=request.user
    ).select_related('categoria')
    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'section_title': 'Productos'  
    })

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            producto = form.save(commit=False)
            # Ensure the product is associated with the current user
            producto.usuario_creador = request.user
            producto.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('productos:lista')
        else:
            messages.error(request, 'Error al crear el producto: ' + ', '.join(form.errors.get('imagen', [])))
    else:
        form = ProductoForm(user=request.user)
    return render(request, 'productos/form_producto.html', {
        'form': form,
        'section_title': 'Nuevo Producto'
    })

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, usuario_creador=request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('productos:lista')
    else:
        form = ProductoForm(instance=producto, user=request.user)
    return render(request, 'productos/form_producto.html', {
        'form': form,
        'object': producto,
        'section_title': 'Editar Producto'
    })

@login_required
def eliminar_producto(request, pk):
    # Only allow deleting products created by the current user
    producto = get_object_or_404(Producto, pk=pk, usuario_creador=request.user)
    if request.method == 'POST':
        producto.delete()
    return redirect('productos:lista')


@login_required
def buscar_productos(request):
    query = request.GET.get('q', '')
    if query:
        # Filter products by both the search query AND the current user
        productos = Producto.objects.filter(
            usuario_creador=request.user,
            nombre__icontains=query
        ).select_related('categoria')
    else:
        # If no query, return all products for the current user
        productos = Producto.objects.filter(
            usuario_creador=request.user
        ).select_related('categoria')
    
    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'section_title': 'Resultados de búsqueda',
        'query': query
    })