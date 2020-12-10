from django.contrib import admin
from .models import Perfil, Plan
# Register your models here.

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipoIdentificacion', 'identificacion', 'telefono')

class PlanAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'iva', 'precio')

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Plan, PlanAdmin)