from django.db import models
from django.conf import settings
from courses.models import Course
# Create your models here.


class Tutorial(models.Model):
    name = models.CharField(blank=False,null=False)
    descriptions = models.TextField(blank= False,null= False)
    started_at = models.DateTimeField(editable=False,)
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="instructor",unique=True)
    course = models.ForeignKey(Course,null= False)
    cost = models.PositiveSmallIntegerField(default = 0)


    class Meta:
        default_permissions = ['add','delete','view',"change"]
        permissions = [("delete_own_tutorial","Can delete own tutorial")]
    


class Video(models.Model):
    title = models.CharField( max_length=50 , blank = False,null = False)
    file = models.Image(null=False)
    duration = models.DurationField(null=False, blank=False)

    class Meta:
        default_permissions = ["view"]
        permissions = [("add_to_own_tutorial","Can add to own tutorial"),]






