from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['codigo', 'nombre', 'razon_social', 'identificacion', 'email', 
                  'telefono', 'direccion', 'ciudad', 'grupo', 'credito', 'estado',
                  'cupo', 'tasa_descuento', 'tasa_recargo', 'comentarios']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese el código...'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese el nombre...'
            }),
            'razon_social': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese la razón social...'
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese la cédula o RUC...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese el email...'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese el teléfono...'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese la dirección...'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese la ciudad...'
            }),
            'grupo': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
            }),
            'credito': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese los días de crédito...'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
            }),
            'cupo': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese el cupo...',
                'step': '0.01'
            }),
            'tasa_descuento': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese la tasa de descuento...',
                'step': '0.01'
            }),
            'tasa_recargo': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese la tasa de recargo...',
                'step': '0.01'
            }),
            'comentarios': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-3 min-h-[120px] focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'placeholder': 'Ingrese comentarios adicionales sobre el cliente...'
            }),
        }
        