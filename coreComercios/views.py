import json
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from coreAdmin.models import Parametro
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion
from .forms import ComercioForm, ProductoForm, ImagenProductoForm, ColeccionForm
from django import forms

# Create your views here.

def home(request):
    return render(request, "codeFrontEnd/home.html")

def consultarDisponibilidadComercio(request, comercio_slug):
    comercio = Comercio.objects.filter(slug=comercio_slug)
    
    if comercio:
        data = {
            'existe': 1,
            'comercio': comercio[0].id,
        }
    else:
        data = {
            'existe': 0
        }
        
    return JsonResponse(data)

def comercio (request, comercio_slug):
    #trae el comercio si existe
    comercio = get_object_or_404(Comercio, slug=comercio_slug)

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)

    # trae los productos relacionados al comercio
    productos = Producto.objects.filter(comercio=comercio.id, estado=True)

    datos = {
        'comercio':comercio,
        'productos':productos,
    }
    return render(request, "codeFrontEnd/comercio.html", datos)

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

    datos = {
        'producto':producto,
        'imagenes_producto':imagenes_producto,
        'comercio':comercio,
        'productos':productos,
    }
    
    return render(request, "codeFrontEnd/producto.html", datos)

# Views administrador

def comercios(request):
    if request.user.is_authenticated:
        comercios = Comercio.objects.filter(owner=request.user)
        datos = {
            'comercios':comercios,
        }
        return render(request, "codeBackEnd/comercios.html", datos)
    else:
        return redirect('login')

class comercioCreateView(CreateView):
    model = Comercio
    form_class = ComercioForm
    template_name = 'codeBackEnd/comercioAdd.html'
    success_url = reverse_lazy('comercioAdmin:comercios' )

class comercioUpdateView(UpdateView):
    model = Comercio
    form_class = ComercioForm
    template_name = 'codeBackEnd/comercio.html'
    
    def get_success_url(self):
        return reverse_lazy('comercioAdmin:comercio', args=[self.object.id]) + '?ok'

def catalogo(request):
    if request.user.is_authenticated:
        parametroLimiteGratis = int(Parametro.objects.filter(parametro="limiteGratis")[0].valor)
        comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
        productos = Producto.objects.filter(comercio=request.session["comercioId"])
        colecciones = Coleccion.objects.filter(comercio=request.session["comercioId"])
        totalProductos = productos.count()

        if comercio.idplan > 0:
            parametroLimiteGratis = 0

        permiteProductos = 0

        if totalProductos < parametroLimiteGratis and parametroLimiteGratis > 0:
            permiteProductos = 1
        
        datos = {
            'colecciones':colecciones,
            'comercio':comercio,
            'permiteProductos':permiteProductos,
        }
        return render(request, "codeBackEnd/catalogo.html", datos)
    else:
        return redirect('login')

def productos(request):
    if request.user.is_authenticated:
        comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
        productos = Producto.objects.filter(comercio=request.session["comercioId"])
        datos = {
            'productos':productos,
            'comercio':comercio,
        }
        return render(request, "codeBackEnd/productos.html", datos)
    else:
        return redirect('login')

class productoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'codeBackEnd/productoAdd.html'
    success_url = reverse_lazy('comercioAdmin:catalogo' )

class productoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'codeBackEnd/producto.html'
    
    def get_success_url(self):
        return reverse_lazy('comercioAdmin:producto', args=[self.object.id]) + '?ok'

class productoDeleteView(DeleteView):
    model = Producto
    template_name = 'codeBackEnd/producto_confirm_delete.html'
    success_url = reverse_lazy('comercioAdmin:catalogo')

def add_image(request):
    if request.method == 'POST':
        pk = request.POST['producto']
        form = ImagenProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            producto = get_object_or_404(Producto, id=pk)
    return redirect('comercioAdmin:producto', pk = producto.id)

def del_image(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        pkImagen = request.POST['pkImagen']
        ImagenesProducto.objects.get(id=pkImagen).imagen.delete(save=True)
        ImagenesProducto.objects.filter(id=pkImagen).delete()
    return redirect('comercioAdmin:producto', pk = pk)

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
    return redirect('comercioAdmin:producto', pk = pk)

class coleccionCreateView(CreateView):
    model = Coleccion
    form_class = ColeccionForm
    template_name = 'codeBackEnd/coleccionAdd.html'
    success_url = reverse_lazy('comercioAdmin:catalogo' )

class coleccionUpdateView(UpdateView):
    model = Coleccion
    form_class = ColeccionForm
    template_name = 'codeBackEnd/coleccion.html'
    
    def get_success_url(self):
        return reverse_lazy('comercioAdmin:coleccionEdit', args=[self.object.id]) + '?ok'

class coleccionDeleteView(DeleteView):
    model = Coleccion
    template_name = 'codeBackEnd/coleccion_confirm_delete.html'
    success_url = reverse_lazy('comercioAdmin:catalogo')
