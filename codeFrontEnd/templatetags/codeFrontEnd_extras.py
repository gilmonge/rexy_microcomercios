from django import template
from coreComercios.models import Comercio, Producto, ImagenesProducto

register = template.Library()

@register.simple_tag
def get_ImagenPrincipal(pkProducto):
    imagen = '/media/productos/noimageProd.jpg'
    
    imagenProd = ImagenesProducto.objects.filter(producto=pkProducto, principal=True)
    if imagenProd:
        imagen = imagenProd[0]
    return imagen

@register.simple_tag
def get_Imagenes(pkProducto):
    imagenesArray = []
    imagen = '/media/productos/noimageProd.jpg'
    
    imagenes = ImagenesProducto.objects.filter(producto=pkProducto, estado=True)
    for img in imagenes:
        if img.producto_id is pkProducto:
            imagenesArray.append(img.imagen.url)

    if not imagenesArray:
        imagenesArray.append(imagen)

    return imagenesArray

@register.simple_tag
def Def_theme(idTheme):
    theme = ''

    if(idTheme == 1):
        theme = 'base'
    elif(idTheme == 2):
        theme = 'dark'
    else:
        pass

    return theme