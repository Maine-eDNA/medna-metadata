from django.apps import AppConfig


class SampleLabelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sample_labels'

    def ready(self):
        from . import signals
