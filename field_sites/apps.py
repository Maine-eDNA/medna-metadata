from django.apps import AppConfig


class FieldSitesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'field_sites'

    def ready(self):
        import field_sites.signals
