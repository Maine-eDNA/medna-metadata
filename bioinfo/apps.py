from django.apps import AppConfig


class BioinfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bioinfo'

    def ready(self):
        import bioinfo.signals
