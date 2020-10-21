from django import template
from coreComercios.models import Comercio, Producto, ImagenesProducto

register = template.Library()

@register.simple_tag
def get_Comercios_list(owner):
    comerciosUsuario = Comercio.objects.filter(owner=owner)
    return comerciosUsuario

@register.simple_tag
def get_Comercio(pk):
    comerciosUsuario = Comercio.objects.filter(id=pk)
    return comerciosUsuario

@register.simple_tag
def get_Imagenes_Producto(pk):
    ImagenesDelProducto = ImagenesProducto.objects.filter(producto=pk)
    return ImagenesDelProducto
