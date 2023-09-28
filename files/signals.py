from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import File








@receiver(post_delete, sender=File)
def remove_file_data(sender, instance, **kwargs):
    instance.url.delete(save = False)

