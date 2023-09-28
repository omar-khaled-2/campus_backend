from django.apps import AppConfig


class QuestionsConfig(AppConfig):
    default_auto_field = 'django.db.models.SmallAutoField'
    name = 'questions'

    def ready(self):
        import questions.signals  
