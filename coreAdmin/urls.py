from django.urls import path
from . import views
from django.views.generic import RedirectView

coreAdmin_patterns = ([
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('comercios/', views.comercios, name="comercios"),
], "coreAdmin")