from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import File,Notification,Folder
import boto3
from user.models import Device
from django.conf import settings
import json
@receiver(post_delete, sender=File)
def remove_file_data(sender, instance, **kwargs):
    instance.url.delete(save = False)



@receiver(post_save,sender = File)
def push_new_file_notificaition(sender,instance,created,**kwargs):
    if not created:
        return
    sns_client = boto3.client('sns')
    topic_name = f"folder-{instance.folder_id}"
    response = sns_client.create_topic(
        Name=topic_name
    )
    topic_arn = response['TopicArn']
    message = json.dumps({
        "default": 'New file added!',
        "GCM": json.dumps({
            "notification": {
                "title": 'New File Added!',
                "body": instance.name
            }
        }),
        "APNS": json.dumps({
            "aps": {
                "alert": {
                    "title": 'New File Added!',
                    "body": instance.name
                }
            }
        })
    })
    sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageStructure = 'json'
    )
    sns_client.close()

@receiver(post_save,sender = Folder)
def create_folder_topic(sender,instance,created,**kwargs):
    if not created:
        return
    sns_client = boto3.client('sns')
    topic_name = f"folder-{instance.id}"
    sns_client.create_topic(
        Name=topic_name
    )
    sns_client.close()


@receiver(post_delete,sender = Folder)
def delete_folder_topic(sender,instance,**kwargs):

    sns_client = boto3.client('sns')
    topic_name = f"folder-{instance.id}"
    response = sns_client.create_topic(
        Name=topic_name
    )
    topic_arn = response['TopicArn']
    sns_client.delete_topic(
        TopicArn=topic_arn
    )
    sns_client.close()




@receiver(post_save, sender=Notification)
def subscribe_folder_notification(sender, instance, **kwargs):
    sns_client = boto3.client('sns')
    user = instance.user
    topic_name = f"folder-{instance.folder_id}"
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
    topic_name = f"folder-{instance.folder_id}"
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
