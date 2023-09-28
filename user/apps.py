from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.SmallAutoField'
    name = 'user'

    def ready(self):
        import user.signals
