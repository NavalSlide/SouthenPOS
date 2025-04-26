from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from .models import Usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario 
class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254, 
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-emerald-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-emerald-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Enter your password'
        })
    )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-emerald-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-emerald-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-emerald-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Enter your last name'
        })
    )

    # Customize password1 and password2 widgets to ensure they render correctly
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-emerald-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Enter your password'
        }),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-emerald-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Confirm your password'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Ensure 'nombre_completo' exists in Usuario model
        user.nombre_completo = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        
        if commit:
            user.save()
        return user