from django.contrib import admin
from .models import Perfil, Plan, Parametro
# Register your models here.

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipoIdentificacion', 'identificacion', 'telefono')

class PlanAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'iva', 'precio')

class ParametroAdmin(admin.ModelAdmin):
    list_display = ('parametro', 'valor', 'detalle')

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Parametro, ParametroAdmin)