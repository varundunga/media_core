from django.apps import AppConfig


class FrontendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.frontend"
    def ready(self):
        import apps.frontend.signals
