from django import template
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion

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
            imagenesArray.append(img)

    if not imagenesArray:
        imagenesArray.append(imagen)

    return imagenesArray

@register.simple_tag
def get_Colecciones(pkComercio):
    collecciones = Coleccion.objects.filter(comercio=pkComercio, estado=True)

    return collecciones

@register.simple_tag
def Def_theme(idPlan):
    theme = ''

    if(idPlan == 0):
        theme = 'base'
    elif(idPlan == 1):
        theme = 'malefashion'
    else:
        pass

    return theme

@register.simple_tag
def encoded_id(id):
    import base64
    Encryptado = base64.b64encode(bytes(str(id), 'ascii'))
    """ Encryptado = str(Encryptado)
    Encryptado.replace("b'", '')
    Encryptado.replace("'", '') """
    return Encryptado.decode("utf-8")

@register.simple_tag
def decode_id(id):
    import base64
    Desencryptado = base64.b64decode(id).decode('utf-8')

    return Desencryptado