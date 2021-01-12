"""microcomercios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from coreComercios.urls import coreComercios_patterns, coreComerciosAdmin_patterns

from django.conf import settings

from coreAdmin.urls import coreAdmin_patterns

from codeHome.urls import codeHome_patterns

urlpatterns = [
    path('DJAdmin/', admin.site.urls),
    path('DJAdmin/clearcache', include('clearcache.urls')),

    # Paths de Admin
    path('comerciosAdmin/', include(coreAdmin_patterns)),
    path('comerciosAdmin/', include(coreComerciosAdmin_patterns)),
    
    # Paths del auth
    path('comerciosAdmin/', include('django.contrib.auth.urls')),


    # Paths del Comercios frontend
    path('', include(coreComercios_patterns)),

    # Paths del home
    path('', include(codeHome_patterns)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)