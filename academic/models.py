from django.db import models
from django.conf import settings



class Term(models.Model):
    name = models.CharField()

class Course(models.Model):
    code = models.CharField(max_length=5,primary_key= True)
    english_name = models.CharField(max_length=30,null=False,blank=False)
    arabic_name = models.CharField(max_length=30,null=False,blank=False)
    credit_hours = models.PositiveSmallIntegerField(null=False,)
    prerequisite = models.ManyToManyField("Course",blank=True)
    def __str__(self):
        return self.english_name
    
    class Meta:
        default_permissions = ["add","delete","view","change"]


class Location(models.Model):
    name = models.CharField(max_length=30,null=False,blank=False)
    building = models.CharField(max_length=30,null=False,blank=False)
    floor = models.PositiveSmallIntegerField()
    description = models.TextField()
    def __str__(self):
        return self.name



class CourseGPA(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False)
    course = models.ForeignKey('Course',on_delete=models.CASCADE,null=False)
    term = models.ForeignKey("Term",on_delete=models.CASCADE,null=False)




class Period(models.Model):    

    start_at = models.TimeField(null=False)
    end_at = models.TimeField(null=False)

    def __str__(self) -> str:
        return "Period {}".format(self.id)




class Activity(models.Model):
    class Activities(models.TextChoices):
        LECTURE = 'Lecture'
        SEMINAR = 'Seminar'
        WORKSHOP = 'Workshop'
        LAB = 'Lab'
        TUTORIAL = 'Tutorial'
        DISCUSSION_GROUP = 'Discussion Group'
        PROJECT_PRESENTATION = 'Project Presentation'
        STUDY_GROUP = 'Study Group'
        EXAMINATION = 'Examination'
        RESEARCH_SEMINAR = 'Research Seminar'
        CONFERENCE = 'Conference'

    
    type = models.CharField(choices=Activities.choices,max_length=30)
    course = models.ForeignKey("Course",on_delete=models.CASCADE,null=False)
    instructor = models.ForeignKey("user.Teacher",on_delete=models.CASCADE,null=False)




    




class Group(models.Model):
    name = models.CharField(max_length=15,blank=False)
    course = models.ForeignKey("Course",on_delete=models.CASCADE,null=False)
    assignments = models.ManyToManyField("assignments.Assignment",blank=True)

    def __str__(self) -> str:
        return f"{self.course.english_name} - {self.name}"


class Schedule(models.Model):
    activity = models.ForeignKey("Activity",on_delete=models.CASCADE,null=False)
    start_period = models.ForeignKey("Period",on_delete=models.CASCADE,related_name="start_period",null=False)
    end_period = models.ForeignKey("Period",on_delete=models.CASCADE,related_name="end_period",null=False)
    location = models.ForeignKey("Location",on_delete=models.CASCADE,null=False)
    groups = models.ManyToManyField("Group",blank=False)
    date = models.DateField(null=False)