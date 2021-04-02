from django import forms
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion, Slider

class ComercioForm(forms.ModelForm):
    class Meta:
        model = Comercio
        fields = ['owner', 'nombre', 'slug', 'eslogan', 'descripcion', 'redessociales', 'contacto', 'img_superior', 'img_acercade', 'logo', 'favicon', 'idplan',]
        
        widgets = {
            'nombre'        : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'slug'          : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre corto'}),
            'eslogan'       : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Eslogan'}),
            'descripcion'   : forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'Descripción'}),
            'redessociales' : forms.Textarea(attrs={'class': 'form-control' , 'placeholder': ''}),
            'contacto'      : forms.Textarea(attrs={'class': 'form-control', 'placeholder': ''}),
            'img_superior'  : forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'img_acercade'  : forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'logo'          : forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'favicon'       : forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }
        
        labels = {
            'img_superior'  : 'Imagen superior ',
            'img_acercade'  : 'Imagen "Acerca de" ',
            'logo'          : 'Logo ',
            'favicon'       : 'Favicon ',
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

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = [ 'comercio', 'titulo', 'subtitulo', 'descripcion', 'boton', 'url', 'imagen', 'target', 'estado' ]
        
        widgets = {
            'titulo'        : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'subtitulo'     : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sub título'}),
            'descripcion'   : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'boton'         : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto Botón'}),
            'url'           : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL del botón'}),
            'imagen'        : forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'target'        : forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Target'}),
            'estado'        : forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Estado'}),
        }

class ColeccionForm(forms.ModelForm):
    class Meta:
        model = Coleccion
        fields = [ 'comercio', 'nombre', 'estado']

        widgets = {
            'nombre'        : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'estado'        : forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Estado'}),
        }