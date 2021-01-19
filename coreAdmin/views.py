from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.http import Http404, JsonResponse
from coreAdmin.forms import UserCreationFormWithEmail
from coreAdmin.models import Parametro, Perfil
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion
from django import forms

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        
        datos = {}
        """ Comprueba que exite el perfil del usuario y sino lo crea """
        existe = Perfil.objects.filter(usuario=request.user).exists()
        if existe == False:
            Perfil.objects.get_or_create(usuario=request.user)

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

def verPlanes(request):
    if request.user.is_authenticated:
        parametroLimiteGratis = Parametro.objects.filter(parametro="limiteGratis")[0].valor
        
        datos = {
            'MaximosProductos':parametroLimiteGratis,
        }

        return render(request, "codeBackEnd/planes.html", datos)
    else:
        return redirect('login')

def verPerfil(request):
    if request.user.is_authenticated:
        usuarioPerfil = Perfil.objects.filter(usuario=request.user)[0]
        
        datos = {
            'usuarioPerfil':usuarioPerfil,
        }

        return render(request, "codeBackEnd/perfil.html", datos)
    else:
        return redirect('login')

def PerfilInformacionEdit(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            usuarioPerfil = Perfil.objects.filter(usuario=request.user)[0]
            usuario = User.objects.filter(id=request.user.id)[0]

            usuario.first_name = request.POST['nombre']
            usuario.last_name = request.POST['apellido']
            usuario.save()

            base_url = reverse('coreAdmin:perfil')
            query_string =  'ok_info'
            url = '{}?{}'.format(base_url, query_string)

            return redirect(url)
        else:
            base_url = reverse('coreAdmin:perfil')
            query_string =  'errorMethod'
            url = '{}?{}'.format(base_url, query_string)

            return redirect('coreAdmin:perfil')
    else:
        return redirect('login')

def PerfilPassEdit(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            
            if request.POST['pass'] == request.POST['confPass']:
                usuario = User.objects.filter(id=request.user.id)[0]
                usuario.set_password(request.POST['pass'])
                usuario.save()

                login(request, usuario)

                base_url = reverse('coreAdmin:perfil')
                query_string =  'ok_pass'
                url = '{}?{}'.format(base_url, query_string)

                return redirect(url)
            else:
                base_url = reverse('coreAdmin:perfil')
                query_string =  'error_01'
                url = '{}?{}'.format(base_url, query_string)

                return redirect(url)
        else:
            base_url = reverse('coreAdmin:perfil')
            query_string =  'errorMethod'
            url = '{}?{}'.format(base_url, query_string)

            return redirect(url)
    else:
        return redirect('login')