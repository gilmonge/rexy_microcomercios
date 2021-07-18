from random import randint
from django import template
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion, OrdenesComercios
from coreAdmin.models import Perfil

register = template.Library()

@register.simple_tag
def get_primerIngreso(user):
    perfil = Perfil.objects.filter(usuario=user)[0]
    return perfil.primerIngreso

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
def get_ProductosColeccion(pkcomercio, pk):
    productos = Producto.objects.filter(
        colecciones__id = pk,
        comercio = pkcomercio
    )[:10]
    return productos

@register.simple_tag
def get_ProductosColeccionTotales(pkcomercio, pk):
    productos = Producto.objects.filter(
        colecciones__id = pk,
        comercio = pkcomercio
    )
    totalProductos = productos.count()
    return totalProductos

@register.simple_tag
def get_TodosProductos(pkcomercio):
    productos = Producto.objects.filter(
        comercio = pkcomercio
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

@register.simple_tag
def get_top10productos(pkcomercio):
    productos = Producto.objects.filter(comercio=pkcomercio).order_by('-visualizaciones')[:10]
    return productos

@register.simple_tag
def get_colorRandom():
    colores = [
        "#177DFF",
        "#FFFFFF",
        "#436FB8",
        "#C7C7C7",
        "#F17073",
        "#F14B4F",
        "#CAC73F",
        "#F1ED4B",
        "#C73FCA",
        "#7ECA7C",
        "#94F1EE",
    ]
    colorSeleccionado = randint(0, len(colores)-1)

    return colores[colorSeleccionado]

@register.simple_tag
def get_ordenesComercio(pkcomercio):
    #from paypal.standard.models import PayPalStandardBase
    ordenes = OrdenesComercios.objects.filter(comercio=pkcomercio)
    
    return ordenes

@register.simple_tag
def get_reCAPTCHA_PUBLIC():
    from django.conf import settings
    
    return settings.RECAPTCHA_PUBLIC