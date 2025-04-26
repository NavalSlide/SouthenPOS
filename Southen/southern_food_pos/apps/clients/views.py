from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm

# Add this import at the top of the file
from django.http import JsonResponse
from django.db.models import Q  # Add this import for Q objects

# Add this view function
def search_clients(request):
    """
    Search for clients by name, identification, or code
    Returns JSON response with matching clients
    """
    term = request.GET.get('term', '')
    
    if len(term) < 2:
        return JsonResponse({'results': []})
    
    # Search for clients that match the term AND belong to the current user
    clients = Cliente.objects.filter(
        Q(nombre__icontains=term) | 
        Q(identificacion__icontains=term) |
        Q(codigo__icontains=term)
    ).filter(estado=True, usuario_creador=request.user)[:10]  # Limit to 10 results
    
    # Format the results
    results = []
    for client in clients:
        results.append({
            'id': client.id,
            'codigo': client.codigo,
            'nombre': client.nombre,
            'identificacion': client.identificacion,
            'direccion': client.direccion,
            'ciudad': client.ciudad
        })
    
    return JsonResponse({'results': results})

def lista_clientes(request):
    # Get query parameters
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'nombre')
    estado_filter = request.GET.get('estado', '')
    
    # Start with clients for the current user only
    clientes = Cliente.objects.filter(usuario_creador=request.user)
    
    # Apply search filter if provided
    if query:
        clientes = clientes.filter(
            nombre__icontains=query
        ) | clientes.filter(
            identificacion__icontains=query
        ) | clientes.filter(
            email__icontains=query
        )
    
    # Apply estado filter if provided
    if estado_filter:
        clientes = clientes.filter(estado=estado_filter)
    
    # Apply sorting
    if sort_by == 'identificacion':
        clientes = clientes.order_by('identificacion')
    elif sort_by == 'email':
        clientes = clientes.order_by('email')
    elif sort_by == 'grupo':
        clientes = clientes.order_by('grupo')
    elif sort_by == 'estado':
        clientes = clientes.order_by('estado')
    else:
        clientes = clientes.order_by('nombre')
    
    context = {
        'clientes': clientes,
        'query': query,
        'sort_by': sort_by,
        'estado_filter': estado_filter,
        'section_title': 'Lista de Clientes'
    }
    
    return render(request, 'clients/lista_clientes.html', context)

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            # Save but don't commit to database yet
            cliente = form.save(commit=False)
            # Associate the client with the current user
            cliente.usuario_creador = request.user
            cliente.save()
            messages.success(request, 'Cliente agregado correctamente.')
            return redirect('clients:lista')
        else:
            # Print form errors if any
            print("Form errors:", form.errors)
    else:
        form = ClienteForm()
    
    return render(request, 'clients/form_cliente.html', {
        'form': form,
        'section_title': 'Agregar Cliente'
    })

def editar_cliente(request, cliente_id):
    # Only allow editing clients created by the current user
    cliente = get_object_or_404(Cliente, id=cliente_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            # Print the form data to see if comentarios is included
            print("Form data:", form.cleaned_data)
            cliente = form.save()
            # Print the saved cliente to verify comentarios was saved
            print("Saved cliente:", cliente.comentarios)
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('clients:lista')
        else:
            # Print form errors if any
            print("Form errors:", form.errors)
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'clients/form_cliente.html', {
        'form': form,
        'cliente': cliente,
        'section_title': 'Editar Cliente'
    })

def eliminar_cliente(request, cliente_id):
    # Only allow deleting clients created by the current user
    cliente = get_object_or_404(Cliente, id=cliente_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('clients:lista')
    
    return render(request, 'clients/eliminar_cliente.html', {
        'cliente': cliente,
        'section_title': 'Eliminar Cliente'
    })

def detalle_cliente(request, cliente_id):
    # Only allow viewing clients created by the current user
    cliente = get_object_or_404(Cliente, id=cliente_id, usuario_creador=request.user)
    
    return render(request, 'clients/detalle_cliente.html', {
        'cliente': cliente,
        'section_title': 'Detalle de Cliente'
    })


def client_search_view(request):
    """
    View to handle AJAX search requests for clients
    """
    search_term = request.GET.get('q', '')
    
    if search_term:
        # Filter by current user
        clients = Cliente.objects.filter(
            Q(nombre__icontains=search_term) | 
            Q(identificacion__icontains=search_term),
            usuario_creador=request.user
        ).values('id', 'nombre', 'identificacion', 'direccion', 'ciudad', 'codigo')
        
        return JsonResponse(list(clients), safe=False)
    
    return JsonResponse([], safe=False)
