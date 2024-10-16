from django.apps import AppConfig


class NvoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nvo"

    def ready(self):
        import nvo.signals
