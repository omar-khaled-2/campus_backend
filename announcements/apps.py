from django.apps import AppConfig


class AnnouncementsConfig(AppConfig):
    default_auto_field = 'django.db.models.SmallAutoField'
    name = 'announcements'

    def ready(self):
        import announcements.signals;