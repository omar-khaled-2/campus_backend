from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Announcement
import boto3
import json




@receiver(post_save, sender=Announcement)
def announcement_created_handler(sender, instance, **kwargs):
    # payload = {
    #     "announcement_id" : instance.id
    # }

    # print(payload);

    # lambda_client = boto3.client('lambda',region_name='eu-west-3')

    # response = lambda_client.invoke(FunctionName='serverless-notifications-dev-announcements',Payload=json.dumps(payload))

    # result = response['Payload'].read()


    # print(result)

    print(instance.id)



@receiver(post_delete, sender=Announcement)
def announcement_deleted_handler(sender, instance, **kwargs):
    if(instance.image):
        instance.image.delete()

