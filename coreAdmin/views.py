from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from coreComercios.models import Comercio, Producto, ImagenesProducto
from .forms import ComercioForm, ProductoForm, ImagenProductoForm

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        
        datos = {}
        if request.session.get('comercioId', None) == "dummy":
            comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
            datos["comercio"] = comercio
        
        return render(request, "coreAdmin/dashboard.html", datos)
    else:
        return redirect('login')

def dashboardSeleccion(request, pk):
    if request.user.is_authenticated:
        request.session["comercioId"] = pk
        
        datos = {}
        if request.session.get('comercioId', None) == "dummy":
            comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
            datos["comercio"] = comercio
        
        return render(request, "coreAdmin/dashboard.html", datos)
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

class comercioUpdateView(UpdateView):
    model = Comercio
    form_class = ComercioForm
    template_name = 'coreAdmin/comercio.html'
    
    def get_success_url(self):
        return reverse_lazy('coreAdmin:comercio', args=[self.object.id]) + '?ok'

def productos(request):
    if request.user.is_authenticated:
        comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
        productos = Producto.objects.filter(comercio=request.session["comercioId"])
        datos = {
            'productos':productos,
            'comercio':comercio,
        }
        return render(request, "coreAdmin/productos.html", datos)
    else:
        return redirect('login')

class productoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'coreAdmin/productoAdd.html'
    success_url = reverse_lazy('coreAdmin:productos' )

class productoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'coreAdmin/producto.html'
    
    def get_success_url(self):
        return reverse_lazy('coreAdmin:producto', args=[self.object.id]) + '?ok'

class productoDeleteView(DeleteView):
    model = Producto
    template_name = 'coreAdmin/producto_confirm_delete.html'
    success_url = reverse_lazy('coreAdmin:productos')

def add_image(request):
    if request.method == 'POST':
        pk = request.POST['producto']
        form = ImagenProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            producto = get_object_or_404(Producto, id=pk)
    return redirect('coreAdmin:producto', pk = producto.id)

def del_image(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        pkImagen = request.POST['pkImagen']
        ImagenesProducto.objects.get(id=pkImagen).imagen.delete(save=True)
        ImagenesProducto.objects.filter(id=pkImagen).delete()
    return redirect('coreAdmin:producto', pk = pk)

def default_image(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        pkImagen = request.POST['pkImagen']

        imagenes = ImagenesProducto.objects.filter(producto=pk)
        for imgProd in imagenes:
            imgProd.principal = 0
            imgProd.save()

        imagen = ImagenesProducto.objects.filter(id=pkImagen)[0]
        imagen.principal = 1
        imagen.save()
        #ImagenesProducto.objects.get(id=pkImagen).imagen.delete(save=True)
        #ImagenesProducto.objects.filter(id=pkImagen).delete()
    return redirect('coreAdmin:producto', pk = pk)
