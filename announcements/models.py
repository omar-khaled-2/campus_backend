from django.db import models
from django.conf import settings
from campus.models import AutoNameImageField



class Announcement(models.Model):
    text = models.TextField(max_length=1000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image = AutoNameImageField(null= True,upload_to="announcements/",blank=True)
    course = models.ForeignKey("academic.Course",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ["add","view","delete","change"]
        permissions = [("delete_own_announcement","Can delete own announcement"),("change_own_announcement","Can change own announcement")]





class Reaction(models.Model):
    class Type(models.TextChoices):
        LIKE = "like",
        DISLIKE = "dislike"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False)
    type = models.CharField(max_length=7, choices=Type.choices,null=False)
    announcement = models.ForeignKey(Announcement,on_delete=models.CASCADE,null=False)

    class Meta:
        default_permissions = []
        permissions = [("react_announcement","can react announcement")]
        unique_together = ["user", "announcement"]


