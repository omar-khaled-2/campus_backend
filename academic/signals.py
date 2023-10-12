from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Course
import boto3
from django.conf import settings
import json




@receiver(post_save, sender=Course)
def create_course_topic(sender, instance,created, **kwargs):
    if not created:
        return
    sns_client = boto3.client('sns')
    topic_name = f"course-{instance.code}"
    sns_client.create_topic(Name=topic_name)
    sns_client.close()

@receiver(post_delete, sender=Course)
def create_course_topic(sender, instance, **kwargs):
    sns_client = boto3.client('sns')
    topic_name = f"course-{instance.code}"
    sns_client.delete_topic(TopicArn=f"arn:aws:sns:eu-west-3:448969029695:{topic_name}")
    sns_client.close()


