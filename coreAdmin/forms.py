from django import forms
from coreComercios.models import Comercio, Producto

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
        fields = [ 'comercio', 'nombre', 'descripcion', 'estado', 'precio' ]

        widgets = {
            'nombre'        : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'descripcion'   : forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'Descripción', 'required': 'true'}),
            'estado'        : forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Estado'}),
            'precio'        : forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Precio'}),
        }