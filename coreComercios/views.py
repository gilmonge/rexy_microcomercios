import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy, reverse
from django.http import Http404, JsonResponse
from coreAdmin.models import Parametro, Perfil
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion, Slider
from .forms import ComercioForm, ProductoForm, ImagenProductoForm, ColeccionForm, SliderForm
from django import forms
import base64

# Create your views here.
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
    try:
        comercio = Comercio.objects.filter(slug=comercio_slug)[0]
    except Comercio.DoesNotExist:
        return render(request, "codeFrontEnd/404.html")

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)
    comercio.ajustes       = json.loads(comercio.ajustes)

    limite = 9 
    if comercio.idplan != 0:
        limite = 12

    # trae los productos relacionados al comercio
    productos = Producto.objects.filter(comercio=comercio.id, estado=True).order_by('-visualizaciones')[:limite]

    # trae los slider relacionados al comercio
    sliders = Slider.objects.filter(comercio=comercio.id, estado=True)

    datos = {
        'comercio':comercio,
        'productos':productos,
        'sliders':sliders,
    }

    return render(request, "codeFrontEnd/comercio.html", datos)

def acercaDe (request, comercio_slug):
    #trae el comercio si existe
    try:
        comercio = Comercio.objects.filter(slug=comercio_slug)[0]
    except Comercio.DoesNotExist:
        return render(request, "codeFrontEnd/404.html")

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)
    comercio.ajustes       = json.loads(comercio.ajustes)
    
    # trae los productos relacionados al comercio

    datos = {
        'comercio':comercio,
    }

    return render(request, "codeFrontEnd/acerca_de.html", datos)

def ComercioProductos (request, comercio_slug):
    #trae el comercio si existe
    try:
        comercio = Comercio.objects.filter(slug=comercio_slug)[0]
    except Comercio.DoesNotExist:
        return render(request, "codeFrontEnd/404.html")

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)
    comercio.ajustes       = json.loads(comercio.ajustes)
    
    # trae los productos relacionados al comercio
    productos_list = Producto.objects.filter(comercio=comercio.id, estado=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(productos_list, 12)

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    datos = {
        'comercio':comercio,
        'productos':productos,
        'totalProductos': paginator.count,
    }

    return render(request, "codeFrontEnd/productos.html", datos)

def ProductosColeccion (request, comercio_slug, pk, coleccion_slug):
    #trae el comercio si existe
    try:
        comercio = Comercio.objects.filter(slug=comercio_slug)[0]
    except Comercio.DoesNotExist:
        return render(request, "codeFrontEnd/404.html")

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)
    comercio.ajustes       = json.loads(comercio.ajustes)

    Desencryptado = int(base64.b64decode(pk).decode('utf-8'))

    # trae los productos relacionados al comercio
    productos_list = Producto.objects.filter(comercio=comercio.id, estado=True, colecciones__id=Desencryptado)

    page = request.GET.get('page', 1)
    paginator = Paginator(productos_list, 12)

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    datos = {
        'comercio':comercio,
        'productos':productos,
        'totalProductos': paginator.count,
    }

    return render(request, "codeFrontEnd/productos.html", datos)

def ComercioProductosBuscar (request, comercio_slug):
    #trae el comercio si existe
    try:
        comercio = Comercio.objects.filter(slug=comercio_slug)[0]
    except Comercio.DoesNotExist:
        return render(request, "codeFrontEnd/404.html")

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)
    comercio.ajustes       = json.loads(comercio.ajustes)
    
    # trae los productos relacionados al comercio
    productos_list = []

    productoSearch = request.GET.get('product', 'sinproducto')

    if productoSearch != '':
        productos_list = Producto.objects.filter(comercio=comercio.id, estado=True, nombre__icontains=productoSearch)
    else:
        return redirect('comercio:productos', comercio_slug = comercio.slug)

    page = request.GET.get('page', 1)
    paginator = Paginator(productos_list, 10)

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    datos = {
        'comercio':comercio,
        'productos':productos,
        'totalProductos': paginator.count,
    }

    return render(request, "codeFrontEnd/productos.html", datos)

def producto(request, comercio_slug, pk, prod_slug):
    # trae el producto si existe
    try:
        try:
            Desencryptado = int(base64.b64decode(pk).decode('utf-8'))
        except:
            return render(request, "codeFrontEnd/404.html")
        producto = Producto.objects.filter(id=Desencryptado).filter(comercio__slug=comercio_slug)
        producto = producto[0]
    except Producto.DoesNotExist:
        return render(request, "codeFrontEnd/404.html")

    producto.visualizaciones = producto.visualizaciones + 1
    producto.save()

    imagenes_producto = ImagenesProducto.objects.select_related('producto').filter(producto=producto.id, estado=True)

    # trae el comercio respectivo al producto
    comercio = Comercio.objects.filter(id=producto.comercio.id)[0]

    # convertimos el contenido json en un diccionario python
    comercio.redessociales = json.loads(comercio.redessociales)
    comercio.contacto      = json.loads(comercio.contacto)
    comercio.ajustes       = json.loads(comercio.ajustes)

    # trae los productos relacionados al comercio
    productos = Producto.objects.filter(comercio=comercio.id, estado=True).exclude(id = Desencryptado).order_by('-visualizaciones')[:4]

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

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)

    def get_success_url(self):
        comercio = Comercio.objects.filter(id=self.object.id)[0]
        usuarioPerfil = Perfil.objects.filter(usuario=comercio.owner)[0]

        usuarioPerfil.primerIngreso = True
        usuarioPerfil.save()

        return reverse_lazy('coreAdmin:dashboardSeleccion', kwargs={'pk': self.object.id})

class comercioUpdateView(UpdateView):
    model = Comercio
    form_class = ComercioForm
    template_name = 'codeBackEnd/comercio.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)
    
    def get_object(self):
        comercio = Comercio.objects.filter(id=self.request.session["comercioId"])[0]
        return comercio

    def get_success_url(self):
        return reverse_lazy('comercioAdmin:comercio') + '?ok'

def catalogo(request):
    if request.user.is_authenticated:
        comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
        productos = Producto.objects.filter(comercio=comercio.id)
        colecciones = Coleccion.objects.filter(comercio=comercio.id)
        totalProductos = productos.count()
        
        datos = {
            'colecciones':colecciones,
            'comercio':comercio,
            'permiteProductos':1,
        }
        return render(request, "codeBackEnd/catalogo.html", datos)
    else:
        return redirect('login')

def configuracion(request):
    if request.user.is_authenticated:
        import datetime
        comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]

        """ Calcula el tiempo restante del plan """
        if comercio.idplan != 0:
            fechaActual = datetime.date.today()
            diasRestantes = (comercio.fechaVencimiento - fechaActual).days
        else:
            diasRestantes = 0
        """ Calcula el tiempo restante del plan """

        datos = {
            'comercio':comercio,
            'diasRestantes':diasRestantes,
        }
        return render(request, "codeBackEnd/configuraciones.html", datos)
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
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)

    def get_success_url(self):
        return reverse_lazy('comercioAdmin:producto', kwargs={ 'pk': encoded_id( self.object.id ) })

class productoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'codeBackEnd/producto.html'
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        Desencryptado = int(base64.b64decode(pk).decode('utf-8'))
        producto = Producto.objects.filter(id=Desencryptado)[0]
        return producto

    def get_success_url(self):
        return reverse_lazy('comercioAdmin:producto', args=[encoded_id(self.object.id)]) + '?ok'

class productoDeleteView(DeleteView):
    model = Producto
    template_name = 'codeBackEnd/producto_confirm_delete.html'
    success_url = reverse_lazy('comercioAdmin:catalogo')
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        Desencryptado = int(base64.b64decode(pk).decode('utf-8'))
        producto = Producto.objects.filter(id=Desencryptado)[0]
        return producto

def add_image(request):
    if request.method == 'POST':
        pk = request.POST['producto']
        form = ImagenProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            producto = get_object_or_404(Producto, id=pk)
    return redirect('comercioAdmin:producto', pk = encoded_id(producto.id))

def del_image(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        pkImagen = request.POST['pkImagen']
        ImagenesProducto.objects.get(id=pkImagen).imagen.delete(save=True)
        ImagenesProducto.objects.filter(id=pkImagen).delete()
    return redirect('comercioAdmin:producto', pk = encoded_id(pk))

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
        
    return redirect('comercioAdmin:producto', pk = encoded_id(pk))

class coleccionCreateView(CreateView):
    model = Coleccion
    form_class = ColeccionForm
    template_name = 'codeBackEnd/coleccionAdd.html'
    success_url = reverse_lazy('comercioAdmin:catalogo' )
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)

class coleccionUpdateView(UpdateView):
    model = Coleccion
    form_class = ColeccionForm
    template_name = 'codeBackEnd/coleccion.html'
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        Desencryptado = int(base64.b64decode(pk).decode('utf-8'))
        coleccion = Coleccion.objects.filter(id=Desencryptado)[0]
        return coleccion

    def get_success_url(self):
        return reverse_lazy('comercioAdmin:coleccionEdit', args=[encoded_id(self.object.id)]) + '?ok'

class coleccionDeleteView(DeleteView):
    model = Coleccion
    template_name = 'codeBackEnd/coleccion_confirm_delete.html'
    success_url = reverse_lazy('comercioAdmin:catalogo')
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        Desencryptado = int(base64.b64decode(pk).decode('utf-8'))
        coleccion = Coleccion.objects.filter(id=Desencryptado)[0]
        return coleccion

def sliderList(request):
    if request.user.is_authenticated:
        comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
        sliders = Slider.objects.filter(comercio=request.session["comercioId"])
        datos = {
            'sliders':sliders,
            'comercio':comercio,
        }
        return render(request, "codeBackEnd/sliders.html", datos)
    else:
        return redirect('login')

class sliderCreateView(CreateView):
    model = Slider
    form_class = SliderForm
    template_name = 'codeBackEnd/sliderAdd.html'
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)

    def get_success_url(self):
        return reverse_lazy('comercioAdmin:slider', kwargs={ 'pk': encoded_id( self.object.id ) })

class sliderUpdateView(UpdateView):
    model = Slider
    form_class = SliderForm
    template_name = 'codeBackEnd/slider.html'
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        Desencryptado = int(base64.b64decode(pk).decode('utf-8'))
        slider = Slider.objects.filter(id=Desencryptado)[0]
        return slider

    def get_success_url(self):
        return reverse_lazy('comercioAdmin:slider', args=[encoded_id(self.object.id)]) + '?ok'

class sliderDeleteView(DeleteView):
    model = Slider
    template_name = 'codeBackEnd/slider_confirm_delete.html'
    success_url = reverse_lazy('comercioAdmin:sliders')
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        else:
            return super().dispatch(request, *args, *kwargs)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        Desencryptado = int(base64.b64decode(pk).decode('utf-8'))
        slider = Slider.objects.filter(id=Desencryptado)[0]
        return slider

# Otras funcionalidades 

def encoded_id(id):
    Encryptado = base64.b64encode(bytes(str(id), 'ascii'))
    """ Encryptado = str(Encryptado)
    Encryptado.replace("b'", '')
    Encryptado.replace("'", '') """
    return Encryptado.decode("utf-8")