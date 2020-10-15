from django.shortcuts import render
from coreComercios.models import Comercio, Producto, ImagenesProducto

# Create your views here.

def dashboard(request):
    return render(request, "coreAdmin/dashboard.html")

def comercios(request):
    comercios = Comercio.objects.filter(owner=request.user)
    datos = {
        'comercios':comercios,
    }
    return render(request, "coreAdmin/comercios.html", datos)