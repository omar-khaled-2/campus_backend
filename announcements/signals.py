from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Announcement
import boto3
import json




@receiver(post_save, sender=Announcement)
def send_notification(sender, instance,created, **kwargs):
    if not created:
        return
    sns_client = boto3.client('sns')
    topic_name = f"course-{instance.course_id}"
    print(f"arn:aws:sns:eu-west-3:448969029695:{topic_name}")


    message = json.dumps({
        "default": 'New Announcement Alert!',
        "GCM": json.dumps({
            "notification": {
                "title": 'New Announcement Alert!',
                "body": instance.text
            }
        }),
        "APNS": json.dumps({
            "aps": {
                "alert": {
                    "title": 'New Announcement Alert!',
                    "body": instance.text
                }
            }
        })
    })

    print(message)

    sns_client.publish(
        TopicArn=f"arn:aws:sns:eu-west-3:448969029695:{topic_name}",
        Message=message,
        MessageStructure = 'json'
    )
    sns_client.close()




@receiver(post_delete, sender=Announcement)
def announcement_deleted_handler(sender, instance, **kwargs):
    if(instance.image):
        instance.image.delete()
    
