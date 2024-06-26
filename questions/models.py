from django.db import models
from django.conf import settings


class Question(models.Model):
    title = models.CharField(blank=False,null= False)
    body = models.TextField(blank=False,null=False)
    course = models.ForeignKey("academic.Course",on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="owner")
    viewer = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="viewer",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        default_permissions = ['add','delete','view',"change"]
        permissions = [("delete_own_question","Can delete own question"),("change_own_question","Can change own question")]




class Comment(models.Model):
    body = models.CharField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        default_permissions = ["add","delete"]







class Answer(models.Model):
    body = models.TextField(blank=False,null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_permissions = ["add","change","delete","view"]
        permissions = [("delete_own_answer","Can delete own answer"),("change_own_answer","Can change own answer")]
        
    



class Vote(models.Model):
    class Type(models.TextChoices):
        UP = "up",
        DOWN = "down"
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=4, choices=Type.choices)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null = True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,null= True)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null= True)

    class Meta:
        default_permissions = []
        permissions = [("vote_answer","Can vote answer"),("vote_question","vote_question")]
        unique_together = ["owner", "question","answer"]



class Approve(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE);
    answer = models.OneToOneField(Answer,on_delete= models.CASCADE)
    
    class Meta:
        default_permissions = []
        permissions = [("approve_answer","can approve answer")]

    


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,null=False)
    class Meta:
        unique_together = ["user", "question"]
        default_permissions = []