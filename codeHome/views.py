import random
from django.shortcuts import render, redirect, get_object_or_404, redirect
from coreAdmin.models import Parametro, Faq
from coreComercios.models import Comercio

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

def help(request):
    faqs = Faq.objects.filter(estado=True)
    datos = {
        'faqs': faqs
    }
    return render(request, "codeHome/help.html", datos)

def clients(request):
    # Trae el id maximo
    max_id = Comercio.objects.order_by('-id')[0].id

    # Genera aleatorios
    listadoRandom = []
    count = 0
    while count < 9:
        random_id = random.randint(1, max_id)
        if random_id not in listadoRandom:
            listadoRandom.append(random_id)
        count += 1

    # trae los comercios segun el orden aleatorio
    Comerciorandom = Comercio.objects.filter(id__in=listadoRandom)

    datos = {
        'comercios': Comerciorandom
    }
    return render(request, "codeHome/clientes.html", datos)