from django.shortcuts import render, redirect
from coreComercios.models import Comercio, Producto, ImagenesProducto

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "coreAdmin/dashboard.html")
    else:
        return redirect('login')

def comercios(request):
    comercios = Comercio.objects.filter(owner=request.user)
    datos = {
        'comercios':comercios,
    }
    return render(request, "coreAdmin/comercios.html", datos)

def comercio(request, pk):
    comercio = Comercio.objects.filter(id=pk)
    datos = {
        'comercio':comercio,
    }
    return render(request, "coreAdmin/comercio.html", datos)

def productos(request, pk):
    comercio = Comercio.objects.filter(id=pk)[0]
    productos = Producto.objects.filter(comercio=pk)
    datos = {
        'productos':productos,
        'comercio':comercio,
    }
    return render(request, "coreAdmin/productos.html", datos)

def producto(request, pk):
    producto = Producto.objects.filter(id=pk)[0]
    comercio = Comercio.objects.filter(id=producto.comercio.id)[0]
    datos = {
        'producto':producto,
        'comercio':comercio,
    }
    return render(request, "coreAdmin/producto.html", datos)