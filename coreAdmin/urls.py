from django.urls import path
from coreAdmin import views as adminViews
from coreAdmin.views import SingUpView
from django.views.generic import RedirectView

coreAdmin_patterns = ([
    path('', adminViews.dashboard, name="dashboard"),
    path('registro/', SingUpView.as_view(), name="signup"),
    path('perfil', adminViews.verPerfil, name="perfil"),
    path('perfil/informacionEdit', adminViews.PerfilInformacionEdit, name="perfilInformacionEdit"),
    path('perfil/passEdit', adminViews.PerfilPassEdit, name="perfilPassEdit"),
    path('<int:pk>', adminViews.dashboardSeleccion, name="dashboardSeleccion"),
    path('seleccionarPlan', adminViews.verPlanes, name="selecPlan"),
], "coreAdmin")