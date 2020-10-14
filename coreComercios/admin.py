from django.contrib import admin
from .models import Comercio, Producto, ImagenesProducto

# Register your models here.

class ComercioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'eslogan', 'owner')

class ImagenesProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'imagen', 'principal', 'estado')

admin.site.register(Comercio, ComercioAdmin)
admin.site.register(Producto)
admin.site.register(ImagenesProducto, ImagenesProductoAdmin)