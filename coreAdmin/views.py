from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from coreAdmin.forms import UserCreationFormWithEmail
from coreAdmin.models import Parametro
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