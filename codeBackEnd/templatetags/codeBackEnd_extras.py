from django import template
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion

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

@register.simple_tag
def get_ProductosColeccion(pk):
    productos = Producto.objects.filter(
        colecciones__id=pk,
    )
    return productos

@register.simple_tag
def get_ImagenPrincipalProd(pkProducto):
    imagen = '/media/productos/noimageProd.jpg'

    ImagenesDelProducto = ImagenesProducto.objects.filter(producto=pkProducto)
    
    for img in ImagenesDelProducto:
        if img.principal is True and img.producto_id is pkProducto:
            imagen = img.imagen.url

    return imagen

@register.simple_tag
def get_colecciones(comercio):
    colecciones = Coleccion.objects.filter(comercio=comercio)

    return colecciones