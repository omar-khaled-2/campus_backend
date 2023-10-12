from django.db.models.signals import post_migrate,post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Device
import boto3
from django.conf import settings
from .models import StudentGroupCourse,OTP
from files.models import Notification

@receiver(post_migrate)
def create_student_groups(sender, **kwargs):
    if sender.name == 'user':
        groups = ['student']
        for group in groups:
            Group.objects.get_or_create(name=group)
 



@receiver(post_save, sender=Device)
def subscrite_courses_notifications(sender, instance,created, **kwargs):
    if not created:
        return
    sns_client = boto3.client('sns')
    response = sns_client.create_platform_endpoint(
        PlatformApplicationArn=settings.FCM_ARN if(instance.platform == 'android') else settings.APNS_ARN,
        Token=instance.token
    )
    endpoint_arn = response['EndpointArn']


    
    course_codes = StudentGroupCourse.objects.filter(student__user = instance.user).values_list('course__code',flat=True)
    for course_code in course_codes:
        topic_name = f"course-{course_code}"
        response = sns_client.create_topic(
            Name=topic_name
        )
        topic_arn = response['TopicArn']
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='application',
            Endpoint=endpoint_arn
        )
    sns_client.close()

@receiver(post_delete, sender=Device)
def unsubscrite_courses_notifications(sender, instance, **kwargs):
    sns_client = boto3.client('sns')
    response = sns_client.create_platform_endpoint(
        PlatformApplicationArn=settings.FCM_ARN if(instance.platform == 'android') else settings.APNS_ARN,
        Token=instance.token
    )
    endpoint_arn = response['EndpointArn']
    
    course_codes = StudentGroupCourse.objects.filter(student__user = instance.user).values_list('course__code',flat=True)
    for course_code in course_codes:
        topic_name = f"course-{course_code}"
        response = sns_client.create_topic(
            Name=topic_name
        )
        topic_arn = response['TopicArn']
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='application',
            Endpoint=endpoint_arn
        )
        sns_client.unsubscribe(
            SubscriptionArn=response["SubscriptionArn"]
        )
    sns_client.close()





@receiver(post_save, sender=Device)
def subscrite_folders_notifications(sender, instance,created, **kwargs):
    if not created:
        return
    sns_client = boto3.client('sns')
    response = sns_client.create_platform_endpoint(
        PlatformApplicationArn=settings.FCM_ARN if(instance.platform == 'android') else settings.APNS_ARN,
        Token=instance.token
    )
    endpoint_arn = response['EndpointArn']    
    folder_ids = Notification.objects.filter(user = instance.user).values_list('folder_id',flat=True)
    for folder_id in folder_ids:
        topic_name = f"folder-{folder_id}"
        response = sns_client.create_topic(
            Name=topic_name
        )
        topic_arn = response['TopicArn']
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='application',
            Endpoint=endpoint_arn
        )
    sns_client.close()

@receiver(post_delete, sender=Device)
def unsubscrite_folders_notifications(sender, instance, **kwargs):
    sns_client = boto3.client('sns')
    response = sns_client.create_platform_endpoint(
        PlatformApplicationArn=settings.FCM_ARN if(instance.platform == 'android') else settings.APNS_ARN,
        Token=instance.token
    )
    endpoint_arn = response['EndpointArn']
    
    folder_ids = Notification.objects.filter(user = instance.user).values_list('folder_id',flat=True)
    for folder_id in folder_ids:
        topic_name = f"folder-{folder_id}"
        response = sns_client.create_topic(
            Name=topic_name
        )
        response = sns_client.create_topic(
            Name=topic_name
        )
        topic_arn = response['TopicArn']
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='application',
            Endpoint=endpoint_arn
        )
        sns_client.unsubscribe(
            SubscriptionArn=response["SubscriptionArn"]
        )
    sns_client.close()






@receiver(post_save, sender = StudentGroupCourse)
def subscribe_to_course(sender,instance,created,**kewargs):
    if not created:
        return

    sns_client = boto3.client('sns')
    topic_name = f"folder-{instance.folder_id}"
    response = sns_client.create_topic(
        Name=topic_name
    )
    topic_arn = response['TopicArn']
    devices = Device.objects.filter(user__student = instance.student)
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



@receiver(post_delete, sender = StudentGroupCourse)
def unsubscribe_to_course(sender,instance,created,**kewargs):
    sns_client = boto3.client('sns')
    topic_name = f"folder-{instance.folder_id}"
    response = sns_client.create_topic(
        Name=topic_name
    )
    topic_arn = response['TopicArn']

    devices = Device.objects.filter(user__student = instance.student)

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


@receiver(post_save, sender = OTP)
def email_otp(sender,instance,created,**kewargs):
    client = boto3.client('ses')
    sender = settings.EMAIL_HOST_USER
    recipient = instance.user.email
    subject = 'Your One-Time Password (OTP)'
    body = f"""
        Dear {instance.user.first_name},

        To ensure the security of your account, we have generated a One-Time Password (OTP) for verification purposes.

        Your OTP is: {instance.secret}

        Please enter this code within the next 3 minutes to complete the verification process. If you did not request this code or have any concerns, please contact our support team immediately.

        Thank you for choosing Campus!

        Best regards,

    """

    client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [recipient],
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': body,
                },
            },
        },
    )
