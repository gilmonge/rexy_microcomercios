from django.urls import path
from coreAdmin import views as adminViews
from django.views.generic import RedirectView

coreAdmin_patterns = ([
    path('', adminViews.dashboard, name="dashboard"),
    path('registro/', adminViews.SingUpView.as_view(), name="signup"),
    path('cuenta', adminViews.verPerfil, name="perfil"),
    path('cuenta/informacionEdit', adminViews.PerfilInformacionEdit, name="perfilInformacionEdit"),
    path('cuenta/passEdit', adminViews.PerfilPassEdit, name="perfilPassEdit"),
    path('<int:pk>', adminViews.dashboardSeleccion, name="dashboardSeleccion"),
    path('seleccionarPlan', adminViews.verPlanes, name="selecPlan"),
    path('checkoutPlan', adminViews.pagarPlan, name="pagarPlan"),
    path('pagoRealizado', adminViews.payment_done, name="payment_done"),
    path('pagoRechazado', adminViews.payment_cancelled, name="payment_cancelled"),
    path('verOrden/<pk>', adminViews.mostrarPdf.as_view(), name="ordenPdfVer"),
    path('cancelarSuscripcion', adminViews.VolverPlanGratis, name="cancelarSuscripcion"),
], "coreAdmin")