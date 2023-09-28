from django.apps import AppConfig


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.SmallAutoField'
    name = 'files'

    def ready(self):
        import files.signals;

