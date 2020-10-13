import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

#funcion de carga de imagen de comercio
def custom_upload_ComercioSup(instance, filename):
    old_instance = Comercio.objects.get(pk=instance.pk)

    # Genera el momento de carga de imagen
    timestamp = datetime.timestamp(datetime.now())

    # Separa el nombre y la extension, lo invierte para pasarlo de primero
    datosImagen = filename.split('.')
    datosImagen.reverse()

    #ruta donde se va a guardar
    ruta = "comercios/{}.{}".format(timestamp, datosImagen[0])

    old_instance.img_superior.delete()
    return ruta

def custom_upload_Comercio(instance, filename):
    old_instance = Comercio.objects.get(pk=instance.pk)

    # Genera el momento de carga de imagen
    timestamp = datetime.timestamp(datetime.now())

    # Separa el nombre y la extension, lo invierte para pasarlo de primero
    datosImagen = filename.split('.')
    datosImagen.reverse()

    #ruta donde se va a guardar
    ruta = "comercios/{}.{}".format(timestamp, datosImagen[0])

    old_instance.img_acercade.delete()
    return ruta

#funcion de carga de imagen de productos
def custom_upload_Producto(instance, filename):
    old_instance = ImagenesProducto.objects.get(pk=instance.pk)

    # Genera el momento de carga de imagen
    timestamp = datetime.timestamp(datetime.now())

    # Separa el nombre y la extension, lo invierte para pasarlo de primero
    datosImagen = filename.split('.')
    datosImagen.reverse()

    #ruta donde se va a guardar
    ruta = "productos/{}.{}".format(timestamp, datosImagen[0])

    old_instance.imagen.delete()
    return ruta

# Create your models here.
class Comercio(models.Model):
    owner           = models.ForeignKey(User, verbose_name="Dueño", on_delete=models.CASCADE)
    nombre          = models.CharField(max_length=100, verbose_name="Nombre")
    slug            = models.CharField(max_length=100, verbose_name="Nombre corto")
    eslogan         = models.CharField(max_length=200, verbose_name="Eslogan del comercio", default="")
    descripcion     = models.TextField(verbose_name="Descripción", default="")
    redessociales   = models.TextField(verbose_name="Redes Sociales")
    contacto        = models.TextField(verbose_name="Contácto")
    img_superior    = models.ImageField(upload_to=custom_upload_ComercioSup, null=False, default="comercios/noimageSup.jpg", verbose_name="Imagen superior")
    img_acercade    = models.ImageField(upload_to=custom_upload_Comercio, null=False, default="comercios/noimageAbout.jpg", verbose_name="Imagen de acerca de")
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    comercio        = models.ForeignKey(Comercio, verbose_name="Comercio", on_delete=models.CASCADE)
    nombre          = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion     = models.TextField(verbose_name="Descripción", default="")
    estado          = models.BooleanField(verbose_name="Estado", default=False)
    moneda          = models.IntegerField(verbose_name="Moneda", default=0)
    precio          = models.DecimalField(verbose_name="Precio", max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.nombre

class ImagenesProducto(models.Model):
    producto    = models.ForeignKey(Producto, verbose_name="Producto asociado", on_delete=models.CASCADE)
    imagen      = models.ImageField(upload_to=custom_upload_Producto, null=False, verbose_name="Imagen del producto", default="productos/noimageProd.jpg")
    principal   = models.BooleanField(verbose_name="Imagen principal", default=False)
    estado      = models.BooleanField(verbose_name="Estado", default=False)
    
    def __str__(self):
        return self.imagen