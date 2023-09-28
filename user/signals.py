from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission


@receiver(post_migrate)
def create_student_groups(sender, **kwargs):
    if sender.name == 'user':
        groups = ['student']
        for group in groups:
            Group.objects.get_or_create(name=group)
 
