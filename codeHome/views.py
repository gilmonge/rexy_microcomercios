from django.shortcuts import render, redirect, get_object_or_404, redirect
from coreAdmin.models import Parametro

# Create your views here.

def home(request):
    parametroLimiteGratis = int(Parametro.objects.filter(parametro="limiteGratis")[0].valor)
    datos = {
        'parametroLimiteGratis':parametroLimiteGratis,
    }
    return render(request, "codeHome/home.html", datos)

def about(request):
    datos = {
    }
    return render(request, "codeHome/about.html", datos)