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

@register.simple_tag
def get_Imagenes(imagenes):
    imagenesArray = []
    imagen = '/media/productos/noimageProd.jpg'
    
    for img in imagenes:
            imagenesArray.append(img.imagen.url)

    if not imagenesArray:
        imagenesArray.append(imagen)

    return imagenesArray