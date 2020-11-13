from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Plan(models.Model):
    nombre      = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción", default="")
    iva         = models.CharField(verbose_name="IVA", max_length=2, default=13)
    precio      = models.DecimalField(verbose_name="Precio", max_digits=12, decimal_places=2)
    opciones    = models.TextField(verbose_name="Opciones", default="")

class Perfil(models.Model):
    usuario             = models.OneToOneField(User, on_delete=models.CASCADE)
    tipoIdentificacion  = models.CharField(verbose_name="Tipo identificacion", max_length=1, default="")
    identificacion      = models.CharField(verbose_name="Identificación", max_length=15, default="")
    telefono            = models.CharField(verbose_name="Teléfono", max_length=15, default="")
    pais                = models.CharField(verbose_name="País", max_length=2, default=0)
    provincia           = models.CharField(verbose_name="Provincia", max_length=4, default=0)
    canton              = models.CharField(verbose_name="Canton", max_length=4, default=0)
    distrito            = models.CharField(verbose_name="Distrito", max_length=4, default=0)
    barrio              = models.CharField(verbose_name="Barrio", max_length=4, default=0)
    direccion           = models.TextField(verbose_name="Dirección", default="")

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Perfil.objects.get_or_create(usuario=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado")