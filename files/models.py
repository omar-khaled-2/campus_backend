from django.db import models
from campus.models import AutoNameFileField

class Folder(models.Model):
    name = models.CharField(blank=False,null=False, max_length=20)
    created_at = models.DateField(editable=False, auto_now=True)
    course = models.ForeignKey("academic.Course",on_delete=models.CASCADE,null=True,blank=True)
    parent = models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True)
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
