import os
from django_resized import ResizedImageField
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from coreAdmin.models import Plan
from paypal.standard.ipn.models import PayPalIPN

#funcion de carga de imagen de comercio
def custom_upload_ComercioSup(instance, filename):
    # Genera el momento de carga de imagen
    timestamp = datetime.timestamp(datetime.now())

    # Separa el nombre y la extension, lo invierte para pasarlo de primero
    datosImagen = filename.split('.')
    datosImagen.reverse()

    #ruta donde se va a guardar
    ruta = "comercios/{}.{}".format(timestamp, datosImagen[0])

    # Borra la imagen anterior en caso de que exista
    if instance.pk is not None:
        old_instance = Comercio.objects.get(pk=instance.pk)
        old_instance.img_superior.delete()

    return ruta

def custom_upload_ComercioLogo(instance, filename):
    # Genera el momento de carga de imagen
    timestamp = datetime.timestamp(datetime.now())

    # Separa el nombre y la extension, lo invierte para pasarlo de primero
    datosImagen = filename.split('.')
    datosImagen.reverse()

    #ruta donde se va a guardar
    ruta = "comercios/{}.{}".format(timestamp, datosImagen[0])

    # Borra la imagen anterior en caso de que exista
    if instance.pk is not None:
        old_instance = Comercio.objects.get(pk=instance.pk)
        old_instance.img_superior.delete()

    return ruta

def custom_upload_ComercioFavicon(instance, filename):
    # Genera el momento de carga de imagen
    timestamp = datetime.timestamp(datetime.now())

    # Separa el nombre y la extension, lo invierte para pasarlo de primero
    datosImagen = filename.split('.')
    datosImagen.reverse()

    #ruta donde se va a guardar
    ruta = "comercios/{}.{}".format(timestamp, datosImagen[0])

    # Borra la imagen anterior en caso de que exista
    if instance.pk is not None:
        old_instance = Comercio.objects.get(pk=instance.pk)
        old_instance.img_superior.delete()

    return ruta

def custom_upload_Comercio(instance, filename):
    # Genera el momento de carga de imagen
    timestamp = datetime.timestamp(datetime.now())

    # Separa el nombre y la extension, lo invierte para pasarlo de primero
    datosImagen = filename.split('.')
    datosImagen.reverse()

    #ruta donde se va a guardar
    ruta = "comercios/{}.{}".format(timestamp, datosImagen[0])

    # Borra la imagen anterior en caso de que exista
    if instance.pk is not None:
        old_instance = Comercio.objects.get(pk=instance.pk)
        old_instance.img_acercade.delete()

    return ruta

#funcion de carga de imagen de productos
def custom_upload_Producto(instance, filename):
    # Genera el momento de carga de imagen
    timestamp = datetime.timestamp(datetime.now())

    # Separa el nombre y la extension, lo invierte para pasarlo de primero
    datosImagen = filename.split('.')
    datosImagen.reverse()

    #ruta donde se va a guardar
    ruta = "productos/{}.{}".format(timestamp, datosImagen[0])

    # Borra la imagen anterior en caso de que exista
    if instance.pk is not None:
        old_instance = ImagenesProducto.objects.get(pk=instance.pk)
        old_instance.imagen.delete()

    return ruta

#funcion de carga de imagen de slider
def custom_upload_slider(instance, filename):
    # Genera el momento de carga de imagen
    timestamp = datetime.timestamp(datetime.now())

    # Separa el nombre y la extension, lo invierte para pasarlo de primero
    datosImagen = filename.split('.')
    datosImagen.reverse()

    #ruta donde se va a guardar
    ruta = "slider/{}.{}".format(timestamp, datosImagen[0])

    # Borra la imagen anterior en caso de que exista
    if instance.pk is not None:
        old_instance = Slider.objects.get(pk=instance.pk)
        old_instance.imagen.delete()

    return ruta


# Create your models here.
class Comercio(models.Model):
    owner           = models.ForeignKey(User, verbose_name="Dueño", on_delete=models.CASCADE)
    nombre          = models.CharField(max_length=100, verbose_name="Nombre")
    slug            = models.CharField(max_length=100, verbose_name="Nombre corto", unique=True)
    eslogan         = models.CharField(max_length=200, verbose_name="Eslogan del comercio", default="")
    descripcion     = models.TextField(verbose_name="Descripción", default="")
    redessociales   = models.TextField(verbose_name="Redes Sociales")
    contacto        = models.TextField(verbose_name="Contácto")
    img_superior    = ResizedImageField(upload_to=custom_upload_ComercioSup, size=[900, 600], quality=100, null=False, default="comercios/noimage.jpg", verbose_name="Imagen superior")
    img_acercade    = ResizedImageField(upload_to=custom_upload_Comercio, size=[900, 600], null=False, default="comercios/noimage.jpg", verbose_name="Imagen de acerca de")
    logo            = ResizedImageField(upload_to=custom_upload_ComercioLogo, size=[400, 144], force_format='PNG', null=False, default="comercios/noimage.jpg", verbose_name="Logo")
    favicon         = ResizedImageField(upload_to=custom_upload_ComercioFavicon, size=[50, 50], force_format='PNG', null=False, default="comercios/noimage.jpg", verbose_name="Favicon")
    idplan          = models.IntegerField(verbose_name="Plan", default="0")
    fechaVencimiento= models.DateField(verbose_name="Fecha vencimiento", blank=True, null=True)
    ajustes         = models.TextField(verbose_name="Otros ajustes", default="{}")
    
    def __str__(self):
        return self.nombre

class Coleccion(models.Model):
    comercio        = models.ForeignKey(Comercio, verbose_name="Comercio", on_delete=models.CASCADE)
    nombre          = models.CharField(max_length=100, verbose_name="Nombre")
    estado          = models.BooleanField(verbose_name="Estado", default=False)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    comercio        = models.ForeignKey(Comercio, verbose_name="Comercio", on_delete=models.CASCADE)
    nombre          = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion     = models.TextField(verbose_name="Descripción", default="")
    estado          = models.BooleanField(verbose_name="Estado", default=False)
    moneda          = models.IntegerField(verbose_name="Moneda", default=0)
    precio          = models.DecimalField(verbose_name="Precio", max_digits=12, decimal_places=2)
    colecciones     = models.ManyToManyField(Coleccion, verbose_name="Colecciones", blank=True)
    visualizaciones = models.IntegerField(verbose_name="Visualizaciones", default="0")
    
    def __str__(self):
        return self.nombre

class ImagenesProducto(models.Model):
    producto    = models.ForeignKey(Producto, verbose_name="Producto asociado", on_delete=models.CASCADE)
    imagen      = ResizedImageField(upload_to=custom_upload_Producto, size=[600, 600], null=False, default="productos/noimage.jpg", verbose_name="Imagen del producto")
    principal   = models.BooleanField(verbose_name="Imagen principal", default=False)
    estado      = models.BooleanField(verbose_name="Estado", default=False)
    
    def __str__(self):
        return self.imagen.url

class Slider(models.Model):
    comercio    = models.ForeignKey(Comercio, verbose_name="Comercio", on_delete=models.CASCADE)
    titulo      = models.CharField(max_length=35, verbose_name="Título")
    subtitulo   = models.CharField(max_length=35, verbose_name="Sub título")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    boton       = models.CharField(max_length=15, verbose_name="Texto del Botón")
    url         = models.CharField(max_length=150, verbose_name="URL del botón")
    imagen      = ResizedImageField(upload_to=custom_upload_slider, size=[1920, 800], force_format='PNG', null=False, verbose_name="Imagen")
    target      = models.BooleanField(verbose_name="Nueva ventana", default=False)
    estado      = models.BooleanField(verbose_name="Estado", default=False)
    
    def __str__(self):
        return self.titulo

class OrdenesComercios(models.Model):
    comercio        = models.ForeignKey(Comercio, verbose_name="Comercio asociado", on_delete=models.DO_NOTHING)
    ipn             = models.ForeignKey(PayPalIPN, verbose_name="Paypal Ipn", on_delete=models.DO_NOTHING)
    plan            = models.ForeignKey(Plan, verbose_name="Plan seleccionado", on_delete=models.DO_NOTHING)
    fechaRealizado  = models.DateField(verbose_name="Fecha realizado", auto_now_add=True)
    fechaVencimiento= models.DateField(verbose_name="Fecha vencimiento", blank=True, null=True)
    
    def __str__(self):
        return self.comercio