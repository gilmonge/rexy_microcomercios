from django.urls import path
from . import views
from .views import comercioUpdateView, productoUpdateView, productoCreateView
from django.views.generic import RedirectView

coreAdmin_patterns = ([
    path('', views.dashboard, name="dashboard"),
    path('comercios/', views.comercios, name="comercios"),
    path('comercio/<int:pk>', comercioUpdateView.as_view(), name="comercio"),
    path('productos/<int:pk>', views.productos, name="productos"),
    path('producto/<int:pk>', productoCreateView.as_view(), name="productosAdd"),
    path('producto/<int:pk>', productoUpdateView.as_view(), name="producto"),
], "coreAdmin")