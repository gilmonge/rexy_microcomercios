from django.shortcuts import render, get_object_or_404
from .models import Comercio, Producto, ImagenesProducto
import json

# Create your views here.

def home(request):
    return render(request, "coreComercios/home.html")

def comercio (request, comercio_slug):
    #trae el comercio si existe
    comercio = get_object_or_404(Comercio, slug=comercio_slug)

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)

    # trae los productos relacionados al comercio
    productos = Producto.objects.filter(comercio=comercio.id, estado=True)
    imagenes = ImagenesProducto.objects.select_related('producto').filter(producto__in=productos, estado=True)

    datos = {
        'comercio':comercio,
        'productos':productos,
        'imagenes':imagenes,
    }
    return render(request, "coreComercios/comercio.html", datos)

def producto(request, comercio_slug, pk, prod_slug):
    # trae el producto si existe
    producto = get_object_or_404(Producto, id=pk)
    imagenes_producto = ImagenesProducto.objects.select_related('producto').filter(producto=producto.id, estado=True)

    # trae el comercio respectivo al producto
    comercio = Comercio.objects.filter(id=producto.comercio.id)[0]

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)

    # trae los productos relacionados al comercio
    productos = Producto.objects.filter(comercio=comercio.id, estado=True).exclude(id = pk)
    imagenes = ImagenesProducto.objects.select_related('producto').filter(producto__in=productos, estado=True)

    datos = {
        'producto':producto,
        'imagenes_producto':imagenes_producto,
        'comercio':comercio,
        'productos':productos,
        'imagenes':imagenes,
    }
    
    return render(request, "coreComercios/producto.html", datos)