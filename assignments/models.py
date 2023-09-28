from django.db import models
from django.conf import settings


class Assignment(models.Model):
    title = models.CharField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    def __str__(self) -> str:
        return self.title
    

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    



class Question(models.Model):
    class QuestionTypes(models.TextChoices):
        MULTIPLE_CHOICE = "MULTIPLE_CHOICE","Multiple Choice"
        CHECKBOX = "CHECKBOX","Checkbox"
        FILE_UPLOAD = "FILE_UPLOAD","File Upload"
        SHORT_ANSWER = "SHORT_ANSWER","Short Answer"
        PARAGRAPH = "PARAGRAPH","Paragraph"

    
    title = models.CharField()
    type = models.CharField(choices=QuestionTypes.choices)
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    




class Option(models.Model):
    text = models.CharField()
    question = models.ForeignKey(Question,on_delete=models.CASCADE)


class Answer(models.Model):

    submission = models.ForeignKey(Submission,on_delete=models.CASCADE)
    option = models.ForeignKey(Option,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    
    

class Files(models.Model):
    file = models.FileField()
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)

    



