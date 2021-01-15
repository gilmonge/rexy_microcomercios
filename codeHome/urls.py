from django.urls import path
from codeHome import views as homeViews

codeHome_patterns = ([
    path('', homeViews.home, name='inicio'),
    path('acerca-de', homeViews.about, name='about'),
], "codeHome")