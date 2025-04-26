from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

# Import your custom form from usuarios app
from apps.usuarios.forms import RegistrationForm
from apps.ventas.models import Venta, DetalleVenta
from apps.clients.models import Cliente
from apps.productos.models import Producto
from apps.transacciones.models import Transaccion  # Add this import
# Import the business model from usuarios app instead
from apps.usuarios.models import Business  # Changed from InformacionNegocio

# Add login view
# Modify the login_view function
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Use the direct URL name for redirection
            return redirect('dashboard')
        else:
            # Authentication failed
            return render(request, 'usuarios/login.html', {'error': 'Credenciales inválidas. Por favor intente de nuevo.'})
    
    return render(request, 'usuarios/login.html')

@login_required
def dashboard(request):
    today = timezone.now().date()
    
    context = {
        'ventas_hoy_pagadas_total': Venta.objects.filter(
            transaccion__fecha__date=today,
            transaccion__procesado_pago=True,
            transaccion__usuario_creador=request.user
        ).aggregate(total=Sum('total'))['total'] or 0,
        
        'ordenes_hoy_pagadas_count': Venta.objects.filter(
            transaccion__fecha__date=today,
            transaccion__procesado_pago=True,
            transaccion__usuario_creador=request.user
        ).count(),
        
        'clientes_nuevos_count': Cliente.objects.filter(
            fecha_registro__date=today,
            usuario_creador=request.user
        ).count(),
        
        'productos_nuevos_count': Producto.objects.filter(
            fecha_creacion__date=today,
            usuario_creador=request.user
        ).count(),
        
        'productos_vendidos_pagados_count': DetalleVenta.objects.filter(
            venta__transaccion__fecha__date=today,
            venta__transaccion__procesado_pago=True,
            venta__transaccion__usuario_creador=request.user
        ).values('producto').distinct().count(),
        
        'ventas_recientes_pagadas': Venta.objects.filter(
            transaccion__procesado_pago=True,
            transaccion__usuario_creador=request.user
        ).order_by('-fecha_hora')[:10],
        
        'productos_mas_vendidos_pagados': Producto.objects.filter(
            detalleventa__venta__transaccion__procesado_pago=True,
            detalleventa__venta__transaccion__usuario_creador=request.user
        ).annotate(
            cantidad_vendida_pagada=Count('detalleventa')
        ).order_by('-cantidad_vendida_pagada')[:5]
    }
    
    return render(request, 'dashboard.html', context)


def register(request):
    if request.method == 'POST':
        # Use your custom RegistrationForm instead of UserCreationForm
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user but don't save to database yet
            user = form.save(commit=False)
            
            # Set username to email if username is empty
            if not user.username:
                user.username = user.email
                
            # Now save the user
            user.save()
            
            # Save many-to-many relationships if any
            form.save_m2m()
            
            # Create or update business information
            business, created = Business.objects.get_or_create(user=user)
            
            # Get business information from the form using the correct field names from the template
            business.nombre_negocio = request.POST.get('nombre_negocio', '')
            business.ruc_negocio = request.POST.get('ruc_negocio', '')
            business.direccion_negocio = request.POST.get('direccion_negocio', '')
            business.ciudad = request.POST.get('ciudad', '')
            business.telefono_negocio = request.POST.get('telefono_negocio', '')
            business.email_negocio = request.POST.get('email_negocio', '')
            
            # Handle logo upload if provided
            if 'logo' in request.FILES:
                business.logo = request.FILES['logo']
                
            business.save()
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'usuarios/register.html', {'form': form})
