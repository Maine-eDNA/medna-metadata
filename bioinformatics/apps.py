from django.apps import AppConfig


class BioinformaticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bioinformatics'

    def ready(self):
        import bioinformatics.signals
