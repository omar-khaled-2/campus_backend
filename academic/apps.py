from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.SmallAutoField'
    name = 'academic'

    def ready(self):
        import academic.signals;
