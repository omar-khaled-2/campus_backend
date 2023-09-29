from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Question,Answer
from .serializers import AnswerSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from django.core.files.storage import default_storage


channel_layer = get_channel_layer()




@receiver(post_delete, sender=Question)
def question_deleted_handler(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(f"question_{instance.id}", {"type": "question_deleted"})



@receiver(post_delete, sender=Question)
def question_file_delete(sender, instance, **kwargs):
        body = json.loads(instance.body)
        for item in body:
            if "insert" in item:
                if "image" in item["insert"] :
                    
                    print(default_storage.delete(item['insert']['image']))
                    print(item['insert']['image'])
                elif "audio" in item["insert"]:
                    default_storage.delete(item['insert']['audio'])
                    print(item['insert']['audio'])



@receiver(post_save, sender=Answer)
def answer_created_handler(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(f"question_{instance.question_id}", {"type": "answer_created", "answer": AnswerSerializer(instance=instance).data})



@receiver(post_delete, sender=Answer)
def answer_deleted_handler(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(f"question_{instance.question_id}", {"type": "answer_deleted", "id": instance.id})


@receiver(post_delete, sender=Answer)
def answer_file_delete(sender, instance, **kwargs):
        body = json.loads(instance.body)
        for item in body:
            if "insert" in item:
                if "image" in item["insert"] :
                    default_storage.delete(item['insert']['image'])
                elif "audio" in item["insert"]:
                    default_storage.delete(item['insert']['audio'])
            

