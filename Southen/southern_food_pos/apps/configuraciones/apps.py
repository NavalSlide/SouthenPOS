from django.apps import AppConfig


class ConfiguracionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.configuraciones'  # Make sure this includes the full path
    verbose_name = 'Configuraciones'
