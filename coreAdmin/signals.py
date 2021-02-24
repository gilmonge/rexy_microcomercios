from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from coreAdmin.views import ProcesarPagoPlan

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        
        #analiza el tipo de pago recibido
        import json
        datosPago = json.loads(ipn.custom)

        if datosPago['tipoPago'] == "PlanMicroComercios":
            # se ha pagado un plan del sistema
            ProcesarPagoPlan(ipn)
            