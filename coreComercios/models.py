from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comercio(models.Model):
    owner           = models.ForeignKey(User, verbose_name="Dueño", on_delete=models.CASCADE)
    nombre          = models.CharField(max_length=100, verbose_name="Nombre")
    slug            = models.CharField(max_length=100, verbose_name="Nombre corto")
    eslogan         = models.CharField(max_length=200, verbose_name="Eslogan del comercio", default="")
    descripcion     = models.TextField(verbose_name="Descripción", default="")
    redessociales   = models.TextField(verbose_name="Redes Sociales")
    contacto        = models.TextField(verbose_name="Contácto")

class Producto(models.Model):
    comercio        = models.ForeignKey(Comercio, verbose_name="Comercio", on_delete=models.CASCADE)
    nombre          = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion     = models.TextField(verbose_name="Descripción", default="")
    estado          = models.BooleanField(verbose_name="Estado", default=False)
    moneda          = models.IntegerField(verbose_name="Moneda", default=0)
    precio          = models.DecimalField(verbose_name="Precio", max_digits=8, decimal_places=2)
    