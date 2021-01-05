import os
from django_resized import ResizedImageField
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from coreAdmin.models import Plan

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

# Create your models here.
class Comercio(models.Model):
    owner           = models.ForeignKey(User, verbose_name="Dueño", on_delete=models.CASCADE)
    nombre          = models.CharField(max_length=100, verbose_name="Nombre")
    slug            = models.CharField(max_length=100, verbose_name="Nombre corto", unique=True)
    eslogan         = models.CharField(max_length=200, verbose_name="Eslogan del comercio", default="")
    descripcion     = models.TextField(verbose_name="Descripción", default="")
    redessociales   = models.TextField(verbose_name="Redes Sociales")
    contacto        = models.TextField(verbose_name="Contácto")
    img_superior    = ResizedImageField(upload_to=custom_upload_ComercioSup, size=[900, 600], null=False, default="comercios/noimageSup.jpg", verbose_name="Imagen superior")
    img_acercade    = ResizedImageField(upload_to=custom_upload_Comercio, size=[500, 433], null=False, default="comercios/noimageAbout.jpg", verbose_name="Imagen de acerca de")
    idplan          = models.IntegerField(verbose_name="Plan", default="0")
    
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
    
    def __str__(self):
        return self.nombre

class ImagenesProducto(models.Model):
    producto    = models.ForeignKey(Producto, verbose_name="Producto asociado", on_delete=models.CASCADE)
    imagen      = ResizedImageField(upload_to=custom_upload_Producto, size=[600, 600], null=False, default="productos/noimageProd.jpg", verbose_name="Imagen del producto")
    principal   = models.BooleanField(verbose_name="Imagen principal", default=False)
    estado      = models.BooleanField(verbose_name="Estado", default=False)
    
    def __str__(self):
        return self.imagen.url