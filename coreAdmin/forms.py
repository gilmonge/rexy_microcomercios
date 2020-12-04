from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion
from coreAdmin.models import Perfil

class ComercioForm(forms.ModelForm):
    class Meta:
        model = Comercio
        fields = ['nombre', 'slug', 'eslogan', 'descripcion', 'redessociales', 'contacto', 'img_superior', 'img_acercade',]
        
        widgets = {
            'nombre'        : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'slug'          : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre corto'}),
            'eslogan'       : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Eslogan'}),
            'descripcion'   : forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'Descripción'}),
            'redessociales' : forms.Textarea(attrs={'class': 'form-control' , 'placeholder': ''}),
            'contacto'      : forms.Textarea(attrs={'class': 'form-control', 'placeholder': ''}),
            'img_superior'  : forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'img_acercade'  : forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }
        
        labels = {
            'img_superior': 'Imagen superior ',
            'img_acercade': 'Imagen "Acerca de" '
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [ 'comercio', 'nombre', 'descripcion', 'estado', 'precio', 'colecciones']

        widgets = {
            'nombre'        : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'descripcion'   : forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'Descripción', 'required': 'true'}),
            'estado'        : forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Estado'}),
            'precio'        : forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Precio'}),
        }

class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = ImagenesProducto
        fields = [ 'producto', 'imagen', 'principal', 'estado' ]
        

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [ "usuario", "tipoIdentificacion", "identificacion", "telefono", "pais", "provincia", "canton", "distrito", "barrio", "direccion" ]

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido, 254 caracteres como máximo y debe ser válido")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ya esta utilizado")
        return email