from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion
from .forms import ComercioForm, ProductoForm, ImagenProductoForm, UserCreationFormWithEmail
from django import forms

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        
        datos = {}
        if request.session.get('comercioId', None) == "dummy":
            comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
            datos["comercio"] = comercio
        
        return render(request, "codeBackEnd/dashboard.html", datos)
    else:
        return redirect('login')

def dashboardSeleccion(request, pk):
    if request.user.is_authenticated:
        request.session["comercioId"] = pk
        
        datos = {}
        if request.session.get('comercioId', None) == "dummy":
            comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
            datos["comercio"] = comercio
        
        return render(request, "codeBackEnd/dashboard.html", datos)
    else:
        return redirect('login')

def comercios(request):
    if request.user.is_authenticated:
        comercios = Comercio.objects.filter(owner=request.user)
        datos = {
            'comercios':comercios,
        }
        return render(request, "codeBackEnd/comercios.html", datos)
    else:
        return redirect('login')

class comercioUpdateView(UpdateView):
    model = Comercio
    form_class = ComercioForm
    template_name = 'codeBackEnd/comercio.html'
    
    def get_success_url(self):
        return reverse_lazy('coreAdmin:comercio', args=[self.object.id]) + '?ok'

def catalogo(request):
    if request.user.is_authenticated:
        comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
        colecciones = Coleccion.objects.filter(comercio=request.session["comercioId"])
        datos = {
            'colecciones':colecciones,
            'comercio':comercio,
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
    success_url = reverse_lazy('coreAdmin:catalogo' )

class productoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'codeBackEnd/producto.html'
    
    def get_success_url(self):
        return reverse_lazy('coreAdmin:producto', args=[self.object.id]) + '?ok'

class productoDeleteView(DeleteView):
    model = Producto
    template_name = 'codeBackEnd/producto_confirm_delete.html'
    success_url = reverse_lazy('coreAdmin:catalogo')

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

class SingUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + "?ok"

    def get_form(self, form_class=None):
        form = super(SingUpView, self).get_form()

        #lo modifico en tiempo real
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Correo electrónico'})
        form.fields['password1'].widget =  forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget =  forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Repite la contraseña'})
        return form

    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return

