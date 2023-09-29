from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db import models
from django.conf import settings

import random
from datetime import datetime, timedelta
import time
from campus.models import AutoNameImageField










class UserManager(BaseUserManager):
    def create_user(self,email, password=None,is_superuser = False, **extra_fields):
        print(email)
        email = self.normalize_email(email=email)
        user = self.model(email=email,is_superuser = is_superuser, **extra_fields,)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email, password=None, **extra_fields):
        return self.create_user(email=email, password = password,is_superuser = True, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,null=False,blank=False)
    profile_pic = AutoNameImageField(upload_to='profile-pics/',default = settings.DEFAULT_PROFILE_PIC)
    first_name = models.CharField(null= False,blank= False)
    last_name = models.CharField(null= False,blank= False)
    saved_announcements = models.ManyToManyField("announcements.Announcement",related_name="saved_announcements",blank=True)
    saved_questions = models.ManyToManyField("questions.Question",related_name="saved_questions",blank=True)


    objects = UserManager()
    
    REQUIRED_FIELDS = ['first_name','last_name']
    USERNAME_FIELD = 'email'


    @property
    def is_staff(self):
       return self.has_perm("can_access_admin_site")
    
    def __str__(self):
        return self.first_name
    

    

class GoogleUser(models.Model):
    user = models.OneToOneField("User",on_delete= models.CASCADE)
    google_id = models.CharField(max_length=24,unique=True)

    class Meta:
        default_permissions = []

    



class Student(models.Model):
    academic_id = models.CharField(primary_key= True,max_length=8)
    user = models.OneToOneField("User",on_delete= models.CASCADE,null=True,blank=True)   
    def __str__(self):
        return self.user.first_name
    
    class Meta:
        default_permissions = ["add","change","delete","view"]
    


class StudentGroupCourse(models.Model):
    student = models.ForeignKey("Student",on_delete= models.CASCADE)
    course = models.ForeignKey("academic.Course",on_delete= models.CASCADE)
    group = models.ForeignKey("academic.Group",on_delete= models.CASCADE)

    class Meta:
        default_permissions = ["add","change","delete","view"]
    



class Teacher(models.Model):
    class Title(models.TextChoices):
        MR = "Mr"
        MRS = "Mrs"
        MISS = "Miss"
        MS = "Ms"
        DR = "Dr"
        PROFESSOR = "Professor"


    name = models.CharField()
    title = models.CharField(choices=Title.choices)
    courses = models.ManyToManyField("academic.Course",blank=True)
    user = models.OneToOneField(User,on_delete= models.CASCADE,null=True,blank=True)

    class Meta:
        default_permissions = ["add","change","delete","view"]
    


    

    def __str__(self):
        return self.title + ". " + self.name
    




class OTP(models.Model):
    secret = models.CharField(max_length=6)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    exp = models.DateTimeField()

    @staticmethod
    def generate(user):
        otp,_ =  OTP.objects.update_or_create(
            user = user,
            defaults={
                "secret":str(random.randint(100000, 999999)),
                "exp":datetime.now() + timedelta(minutes=3)
            }
        )
        
        return otp
    
    class Meta:
        default_permissions = []
    


class DeviceToken(models.Model):
    user = models.OneToOneField("User",on_delete=models.CASCADE)
    device_token = models.CharField(max_length=200)
    class Meta:
        default_permissions = []
    