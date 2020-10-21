from django.urls import path
from . import views
from .views import comercioUpdateView, productoUpdateView, productoCreateView, productoDeleteView
from django.views.generic import RedirectView

coreAdmin_patterns = ([
    path('', views.dashboard, name="dashboard"),
    path('<int:pk>', views.dashboardSeleccion, name="dashboardSeleccion"),
    path('comercios/', views.comercios, name="comercios"),
    path('comercio/<int:pk>', comercioUpdateView.as_view(), name="comercio"),
    path('productos', views.productos, name="productos"),
    path('producto/<int:pk>', productoUpdateView.as_view(), name="producto"),
    path('productoAdd', productoCreateView.as_view(), name="productosAdd"),
    path('productoDel/<int:pk>', productoDeleteView.as_view(), name="productoDelete"),
    path('productoImagenAdd', views.add_image, name="productoImagenAdd"),
    path('productoImagenDel', views.del_image, name="productoImagenDel"),
    path('productoImagenDef', views.default_image, name="productoImagenDef"),
], "coreAdmin")