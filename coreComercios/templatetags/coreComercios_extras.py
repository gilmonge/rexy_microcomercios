from django import template
from coreComercios.models import Comercio, Producto, ImagenesProducto

register = template.Library()

@register.simple_tag
def get_ImagenPrincipal(imagenes, pkProducto):
    imagen = '/media/productos/noimageProd.jpg'
    
    for img in imagenes:
        if img.principal is True and img.producto_id is pkProducto:
            imagen = img.imagen.url

    return imagen