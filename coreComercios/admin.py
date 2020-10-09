from django.contrib import admin
from .models import Comercio,Producto

# Register your models here.

class ComercioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'eslogan', 'owner')

admin.site.register(Comercio, ComercioAdmin)
admin.site.register(Producto)