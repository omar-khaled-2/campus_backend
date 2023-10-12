from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Question,Answer,Notification
from .serializers import AnswerSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from django.core.files.storage import default_storage
import boto3
from django.conf import settings
from user.models import Device

channel_layer = get_channel_layer()




@receiver(post_delete, sender=Question)
def notify_users_question_deleted(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(f"question_{instance.id}", {"type": "question_deleted"})



@receiver(post_delete, sender=Question)
def question_delete_files_handler(sender, instance, **kwargs):
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
def notify_users_answer_created(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(f"question_{instance.question_id}", {"type": "answer_created", "answer": AnswerSerializer(instance=instance).data})



@receiver(post_delete, sender=Answer)
def notify_users_answer_deleted(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(f"question_{instance.question_id}", {"type": "answer_deleted", "id": instance.id})


@receiver(post_delete, sender=Answer)
def answer_delete_files_handler(sender, instance, **kwargs):
        body = json.loads(instance.body)
        for item in body:
            if "insert" in item:
                if "image" in item["insert"] :
                    default_storage.delete(item['insert']['image'])
                elif "audio" in item["insert"]:
                    default_storage.delete(item['insert']['audio'])
            


@receiver(post_save,sender = Question)
def create_topic_question(sender,instance,created,**kwargs):
    if not created:
        return
    sns_client = boto3.client('sns')
    topic_name = f"question-{instance.code}"
    sns_client.create_topic(Name=topic_name)
    sns_client.close()
    Notification.objects.create(question = instance,user = instance.owner)


@receiver(post_delete,sender = Question)
def delete_topic_question(sender,instance,created,**kwargs):
    if not created:
        return
    sns_client = boto3.client('sns')
    topic_name = f"question-{instance.code}"
    response = sns_client.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    sns_client.delete_topic(TopicArn=topic_arn)
    sns_client.close()



@receiver(post_save, sender=Notification)
def subscribe_question_notification(sender, instance, **kwargs):
    sns_client = boto3.client('sns')
    user = instance.user
    topic_name = f"question-{instance.question_id}"
    response = sns_client.create_topic(
        Name=topic_name
    )
    topic_arn = response['TopicArn']
    devices = Device.objects.filter(user = user);
    for device in devices:
        response = sns_client.create_platform_endpoint(
            PlatformApplicationArn=settings.FCM_ARN if(device.platform == 'android') else settings.APNS_ARN,
            Token=device.token
        )
        endpoint_arn = response['EndpointArn']
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='application',
            Endpoint=endpoint_arn
        )
    sns_client.close()


@receiver(post_delete, sender=Notification)
def unsubscribe_folder_notification(sender, instance, **kwargs):
    sns_client = boto3.client('sns')
    user = instance.user
    topic_name = f"questions-{instance.question_id}"
    response = sns_client.create_topic(
        Name=topic_name
    )
    topic_arn = response['TopicArn']
    devices = Device.objects.filter(user = user)
    for device in devices:
        response = sns_client.create_platform_endpoint(
            PlatformApplicationArn=settings.FCM_ARN if(device.platform == 'android') else settings.APNS_ARN,
            Token=device.token
        )
        endpoint_arn = response['EndpointArn']
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='application',
            Endpoint=endpoint_arn
        )
        sns_client.unsubscribe(
            SubscriptionArn=response["SubscriptionArn"]
        )

    sns_client.close()


