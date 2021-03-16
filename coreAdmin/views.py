import requests
import json
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.views import View
from coreAdmin.forms import UserCreationFormWithEmail
from coreAdmin.models import Parametro, Perfil, Plan
from coreComercios.models import Comercio, Producto, ImagenesProducto, Coleccion, OrdenesComercios
from django import forms
from xhtml2pdf import pisa

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        perfil =  None
        datos = {}
        """ Comprueba que exite el perfil del usuario y sino lo crea """
        existe = Perfil.objects.filter(usuario=request.user).exists()

        if existe == False:
            Perfil.objects.get_or_create(usuario=request.user)

            return redirect('comercioAdmin:comercioAdd')
        else:
            perfil = Perfil.objects.get_or_create(usuario=request.user)[0]

        if request.session.get('comercioId', None) == "dummy":
            comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
            datos["comercio"] = comercio

        if perfil.primerIngreso is False:
            return redirect('comercioAdmin:comercioAdd')
        else:
            return render(request, "codeBackEnd/dashboard.html", datos)
        
    else:
        return redirect('login')

def dashboardSeleccion(request, pk):
    if request.user.is_authenticated:
        request.session["comercioId"] = pk
        
        datos = {}
        if request.session.get('comercioId', None) == "dummy":
            comercio = Comercio.objects.filter(id=request.session["comercioId"])[0]
            datos["comercio"] = comercio
        
        return render(request, "codeBackEnd/dashboard.html", datos)
    else:
        return redirect('login')

class SingUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + "?ok"

    def get_form(self, form_class=None):
        form = super(SingUpView, self).get_form()

        #lo modifico en tiempo real
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Correo electrónico'})
        form.fields['password1'].widget =  forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget =  forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Repite la contraseña'})
        return form

    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return

def verPlanes(request):
    if request.user.is_authenticated:
        parametroLimiteGratis = Parametro.objects.filter(parametro="limiteGratis")[0].valor
        
        datos = {
            'MaximosProductos':parametroLimiteGratis,
        }

        return render(request, "codeBackEnd/planes.html", datos)
    else:
        return redirect('login')

def pagarPlan(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            idPlan = request.POST["idPlan"]
            form = {}

            if idPlan == '0':
                parametroLimiteGratis = Parametro.objects.filter(parametro="limiteGratis")[0].valor
                datosPlan = {
                    "{limite} productos máximo".format(limite = parametroLimiteGratis),
                    "Plantilla básica",
                }
                nombrePlan = "Gratis"
                costoPlan = 0
            else:
                datosPlan = {
                    "Productos ilimitados",
                    "Plantilla básica",
                    "Plantilla adicionales que se vayan habilitando",
                }
                nombrePlan = "Pyme"
                costoPlan = 5

                """ Requiere realizar el boton de paypal """
                from django.conf import settings
                from decimal import Decimal
                from paypal.standard.forms import PayPalPaymentsForm

                settings.PAYPAL_RECEIVER_EMAIL = Parametro.objects.filter(parametro="PAYPAL_RECEIVER_EMAIL")[0].valor
                settings.PAYPAL_TEST = Parametro.objects.filter(parametro="PAYPAL_TEST")[0].valor

                host = request.get_host()

                # estructur los datos para su posterior manipulacion
                import json
                
                DatosPlanPaypal = {
                    # tipo de pago recibido
                    "tipoPago"  : "PlanMicroComercios",

                    # Datos del plan
                    "idPlan"    : idPlan,
                    "precio"    : costoPlan,

                    # Datos del comercio
                    "comercio"  : request.session["comercioId"],
                    "cliente"   : request.user.id,
                }

                paypal_dict = {
                    "business"      : settings.PAYPAL_RECEIVER_EMAIL,
                    "amount"        : '%.2f' % costoPlan,
                    "item_name"     : 'Plan a pagar {}'.format(nombrePlan),
                    "currency_code" : 'USD',
                    "custom"        : DatosPlanPaypal,#json.dumps()
                    "notify_url"    : 'https://{}{}'.format(host, reverse('paypal-ipn')),
                    "return_url"    : 'https://{}{}'.format(host, reverse('coreAdmin:payment_done')),
                    "cancel_return" : 'https://{}{}'.format(host, reverse('coreAdmin:payment_cancelled')),
                }

                form = PayPalPaymentsForm(initial=paypal_dict)

                """ Requiere realizar el boton de paypal """

            datos = {
                'idPlan': idPlan,
                'datosPlan': datosPlan,
                'nombrePlan': nombrePlan,
                'form': form,
                'costoPlan': costoPlan,
            }

            return render(request, "codeBackEnd/planes_checkout.html", datos)
        else:
            return redirect('coreAdmin:selecPlan')
    else:
        return redirect('login')

@csrf_exempt
def payment_done(request):
    if request.user.is_authenticated:
        datos = {}
        return render(request, "codeBackEnd/payment_done.html", datos)
    else:
        return redirect('login')

@csrf_exempt
def payment_cancelled(request):
    if request.user.is_authenticated:
        datos = {}
        return render(request, "codeBackEnd/payment_cancelled.html", datos)
    else:
        return redirect('login')

def verPerfil(request):
    if request.user.is_authenticated:
        usuarioPerfil = Perfil.objects.filter(usuario=request.user)[0]
        
        datos = {
            'usuarioPerfil':usuarioPerfil,
        }

        return render(request, "codeBackEnd/perfil.html", datos)
    else:
        return redirect('login')

def PerfilInformacionEdit(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            usuarioPerfil = Perfil.objects.filter(usuario=request.user)[0]
            usuario = User.objects.filter(id=request.user.id)[0]

            usuario.first_name = request.POST['nombre']
            usuario.last_name = request.POST['apellido']
            usuario.save()

            base_url = reverse('coreAdmin:perfil')
            query_string =  'ok_info'
            url = '{}?{}'.format(base_url, query_string)

            return redirect(url)
        else:
            base_url = reverse('coreAdmin:perfil')
            query_string =  'errorMethod'
            url = '{}?{}'.format(base_url, query_string)

            return redirect('coreAdmin:perfil')
    else:
        return redirect('login')

def PerfilPassEdit(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            
            if request.POST['pass'] == request.POST['confPass']:
                usuario = User.objects.filter(id=request.user.id)[0]
                usuario.set_password(request.POST['pass'])
                usuario.save()

                login(request, usuario)

                base_url = reverse('coreAdmin:perfil')
                query_string =  'ok_pass'
                url = '{}?{}'.format(base_url, query_string)

                return redirect(url)
            else:
                base_url = reverse('coreAdmin:perfil')
                query_string =  'error_01'
                url = '{}?{}'.format(base_url, query_string)

                return redirect(url)
        else:
            base_url = reverse('coreAdmin:perfil')
            query_string =  'errorMethod'
            url = '{}?{}'.format(base_url, query_string)

            return redirect(url)
    else:
        return redirect('login')

def VolverPlanGratis(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            comercio = Comercio.objects.filter(pk=request.session["comercioId"])[0]
            comercio.fechaVencimiento = None
            comercio.idplan = 0
            comercio.save()

            base_url = reverse('comercioAdmin:configuracion')
            return redirect(base_url)

        else:
            base_url = reverse('comercioAdmin:configuracion')

            return redirect(base_url)
    else:
        return redirect('login')

class mostrarPdf(View):
    def get(self, request, *args, **kwargs): 
        import base64
        try:
            Desencryptado = int(base64.b64decode(kwargs["pk"]).decode('utf-8'))
        except:
            return render(request, "codeFrontEnd/404.html")
            
        from microcomercios import settings
        orden = OrdenesComercios.objects.filter(pk=Desencryptado)[0]
        
        protocoloHttp = "https://"
        if settings.DEBUG == True:
            protocoloHttp = "http://"

        context = {
            "host" : "{}{}".format(protocoloHttp, request.get_host()),
            "orden": orden,
        }

        pdf = render_to_pdf("codeBackEnd/pdf.html", context)
        return HttpResponse(pdf, content_type='application/pdf')

# otras funciones

def ProcesarPagoPlan(ipn):
    import json
    datoPago = json.loads(ipn.custom)
    
    # calcula la fecha de vencimiento del plan
    fechaVencimiento = CalcularMes()

    # {'tipoPago': 'PlanMicroComercios', 'idPlan': '1', 'precio': 5, 'comercio': 1, 'cliente': 1}
    comercio = Comercio.objects.filter(id=datoPago['comercio'])[0]
    planComprado = Plan.objects.filter(id=datoPago['idPlan'])[0]

    comercio.idplan = datoPago['idPlan']
    comercio.fechaVencimiento = fechaVencimiento
    comercio.save()

    # genera la orden
    Orden = OrdenesComercios(
        comercio        = comercio,
        ipn             = ipn,
        plan            = planComprado,
        fechaVencimiento= fechaVencimiento,
    )
    Orden.save()

def CalcularMes():
    """ Calcula un mes a partir del dia de ejecucion """
    from datetime import date
    current_date=date.today()
    carry, new_month=divmod(current_date.month-1+1, 12)
    new_month+=1
    fechaVencimiento=current_date.replace(year=current_date.year+carry, month=new_month)
    """ Calcula un mes a partir del dia de ejecucion """
    return fechaVencimiento

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def onLogin(request):
    ErrorRequest = reverse_lazy('login') + "?error"
    if request.method!="POST":
        return redirect(ErrorRequest)
    else:
        """ reCaptcha """
        if validaReCaptcha(request.POST.get("g-recaptcha-response"))==False:
            return redirect(ErrorRequest)
        """ reCaptcha """
        
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        print(ErrorRequest)
        if user is not None:
            login(request, user)
            return redirect('coreAdmin:dashboard')
        else:
            return redirect(ErrorRequest)

def onRegister(request):
    ErrorRequest = reverse_lazy('coreAdmin:signup') + "?error"
    
    if request.method!="POST":
        return redirect(ErrorRequest)
    else:
        """ reCaptcha """
        if validaReCaptcha(request.POST.get("g-recaptcha-response"))==False:
            return redirect(ErrorRequest)
        """ reCaptcha """
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")

        if password1 == password2:
            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
                user.save()
                messages.success(request,"Successfully Created Admin")
                return HttpResponseRedirect(reverse("show_login"))
            except:
                return redirect(ErrorRequest)
        else:
            return redirect(ErrorRequest)


def validaReCaptcha(captcha_token):
    """ reCaptcha """
    from django.conf import settings

    cap_url="https://www.google.com/recaptcha/api/siteverify"
    
    cap_data={
        "secret":settings.RECAPTCHA_PRIVATE,
        "response":captcha_token
    }
    cap_server_response=requests.post(url=cap_url,data=cap_data)
    cap_json=json.loads(cap_server_response.text)

    return cap_json['success']
    """ reCaptcha """