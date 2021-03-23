from django.urls import path, re_path
from django.views.generic import RedirectView
from coreComercios import views
from coreComercios.views import comercioUpdateView, comercioCreateView, \
    productoUpdateView, productoCreateView, productoDeleteView, \
    coleccionUpdateView, coleccionCreateView, coleccionDeleteView
    

coreComercios_patterns = ([
    path('<slug:comercio_slug>/', views.comercio, name='comercio'),
    path('<slug:comercio_slug>/acerca-de', views.acercaDe, name='acercaDe'),
    path('<slug:comercio_slug>/productos', views.ComercioProductos, name='productos'),
    path(r'<slug:comercio_slug>/p/<pk>/<slug:prod_slug>/', views.producto, name="producto"),
], "comercio")
    
coreComerciosAdmin_patterns = ([
    # administrador
    path('comercios/', views.comercios, name="comercios"),
    path('comercio', comercioUpdateView.as_view(), name="comercio"),
    path('comercioAdd', comercioCreateView.as_view(), name="comercioAdd"),
    path('comercioDisponibilidad/<slug:comercio_slug>', views.consultarDisponibilidadComercio, name="comercioDisponibilidad"),
    
    path('catalogo', views.catalogo, name="catalogo"),
    path('configuracion', views.configuracion, name="configuracion"),
    path('coleccion/<pk>', coleccionUpdateView.as_view(), name="coleccionEdit"),
    path('coleccionAdd', coleccionCreateView.as_view(), name="coleccionAdd"),
    path('coleccionDel/<pk>', coleccionDeleteView.as_view(), name="coleccionDelete"),
    path('productos', views.productos, name="productos"),
    path('producto/<pk>', productoUpdateView.as_view(), name="producto"),
    path('productoAdd', productoCreateView.as_view(), name="productosAdd"),
    path('productoDel/<pk>', productoDeleteView.as_view(), name="productoDelete"),
    path('productoImagenAdd', views.add_image, name="productoImagenAdd"),
    path('productoImagenDel', views.del_image, name="productoImagenDel"),
    path('productoImagenDef', views.default_image, name="productoImagenDef"),
], "comercioAdmin")
