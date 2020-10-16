from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from coreComercios.models import Comercio, Producto, ImagenesProducto
from .forms import ComercioForm

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "coreAdmin/dashboard.html")
    else:
        return redirect('login')

def comercios(request):
    if request.user.is_authenticated:
        comercios = Comercio.objects.filter(owner=request.user)
        datos = {
            'comercios':comercios,
        }
        return render(request, "coreAdmin/comercios.html", datos)
    else:
        return redirect('login')

def comercio(request, pk):
    comercio = Comercio.objects.filter(id=pk)
    datos = {
        'comercio':comercio,
    }
    return render(request, "coreAdmin/comercio.html", datos)

class comercioUpdateView(UpdateView):
    model = Comercio
    form_class = ComercioForm
    #template_name_suffix = '_update_form'
    template_name = 'coreAdmin/comercio.html'
    
    def get_success_url(self):
        return reverse_lazy('coreAdmin:comercio', args=[self.object.id]) + '?ok'

def productos(request, pk):
    if request.user.is_authenticated:
        comercio = Comercio.objects.filter(id=pk)[0]
        productos = Producto.objects.filter(comercio=pk)
        datos = {
            'productos':productos,
            'comercio':comercio,
        }
        return render(request, "coreAdmin/productos.html", datos)
    else:
        return redirect('login')

def producto(request, pk):
    if request.user.is_authenticated:
        producto = Producto.objects.filter(id=pk)[0]
        comercio = Comercio.objects.filter(id=producto.comercio.id)[0]
        datos = {
            'producto':producto,
            'comercio':comercio,
        }
        return render(request, "coreAdmin/producto.html", datos)
    else:
        return redirect('login')