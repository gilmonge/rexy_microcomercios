from django.shortcuts import render, get_object_or_404
from .models import Comercio
import json

# Create your views here.

def home(request):
    return render(request, "coreComercios/home.html")

def comercio (request, comercio_slug):
    comercio = get_object_or_404(Comercio, slug=comercio_slug)

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)

    datos = {
        'comercio':comercio,
    }
    return render(request, "coreComercios/comercio.html", datos)

def producto(request, pk, prod_slug):
    return render(request, "coreComercios/producto.html")