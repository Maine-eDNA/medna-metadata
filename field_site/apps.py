from django.apps import AppConfig


class FieldSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'field_site'

    def ready(self):
        import field_site.signals
