import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path,path,include
from questions.consumers import QuestionConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        re_path(r'questions/(?P<question_id>\d+)',QuestionConsumer.as_asgi())
    ])
})
