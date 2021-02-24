from django.apps import AppConfig


class CoreadminConfig(AppConfig):
    name = 'coreAdmin'

    # importar para recibir las señales de paypal
    def ready(self):
        import coreAdmin.signals