from django.urls import path
from . import views

coreComercios_patterns = ([
    path('', views.home, name='inicio'),
    path('<slug:comercio_slug>/', views.comercio, name='comercio'),
    path('<int:pk>/<slug:prod_slug>/',   views.producto, name="producto"),
    #path('buscar/',   blog_filterListView.as_view(), name="search"),
    #path('categoria/<int:pk>/<slug:post_slug>/',   category_filterListView.as_view(), name="category"),
    #path('reciente/', views.reciente_post, name="reciente"),
], "comercio") 