from django import forms
from .models import Producto, Categoria
from django.core.validators import FileExtensionValidator

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded-lg'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'stock', 'categoria', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded-lg'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': '0'}),
            'precio': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'step': '0.01', 'min': '0'}),
        }
        
    imagen = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ],
        widget=forms.FileInput(attrs={
            'accept': 'image/jpeg, image/png',
            'class': 'form-image-input'
        }),
        help_text="Formatos aceptados: JPG, JPEG, PNG. Tamaño máximo: 2MB"
    )

    def clean_imagen(self):
        image = self.cleaned_data.get('imagen')
        if image:
            # Validate file size (2MB max)
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("El tamaño máximo permitido es 2MB")
            # Validate actual image format using Pillow
            try:
                from PIL import Image
                img = Image.open(image)
                img.verify()
            except (IOError, ImportError):
                raise forms.ValidationError("Formato de imagen inválido")
        return image

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario_creador=user).order_by('nombre')
        else:
            self.fields['categoria'].queryset = Categoria.objects.none()
            
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.none(),  # Will be set in __init__
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
        required=False
    )