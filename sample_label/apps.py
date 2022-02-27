from django.apps import AppConfig


class SampleLabelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sample_label'

    def ready(self):
        import sample_label.signals
