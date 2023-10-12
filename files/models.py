from django.db import models
from campus.models import AutoNameFileField
from django.conf import settings

class Folder(models.Model):
    name = models.CharField(blank=False,null=False, max_length=20)
    created_at = models.DateField(editable=False, auto_now=True)
    course = models.ForeignKey("academic.Course",on_delete=models.CASCADE,null=True,blank=True)
    parent = models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    class Meta:
        default_permissions = ["add","delete","view"]
        


class File(models.Model):
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE,null=False)
    url = AutoNameFileField(null=False,upload_to='files/')
    created_at = models.DateField(editable=False, auto_now=True)
    size = models.PositiveIntegerField(editable=False)
    class Meta:
        default_permissions = ["add","delete"]

    def save(self, *args, **kwargs):  
        self.size = self.url.size
        super(File, self).save(*args, **kwargs)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False,related_name="folder_notificaitons")
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE,null=False)
    class Meta:
        default_permissions = []
        unique_together = ["user", "folder"]

