from django import template
from coreComercios.models import Comercio, Producto
from coreAdmin.models import Perfil

register = template.Library()

@register.simple_tag
def get_Contadores():
    Comercios = Comercio.objects.all().count()
    Productos = Producto.objects.all().count()
    Perfiles  = Perfil.objects.all().count()
    
    contadores = {
        'Comercios':Comercios,
        'Productos':Productos,
        'Perfiles' :Perfiles,
    }
    return contadores
