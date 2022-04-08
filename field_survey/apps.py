from django.apps import AppConfig


class FieldSurveyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'field_survey'

    def ready(self):
        import field_survey.signals
