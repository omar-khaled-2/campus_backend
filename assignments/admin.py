from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple, Type, Union
from django.contrib import admin
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.http.request import HttpRequest
from campus_admin.views import campusAdminSite
from .models import Assignment, Submission,Question,Option
from django import forms



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if True:
            self.fields['options'] = forms.MultipleChoiceField(choices=["ss"])





class QuestionInline(admin.StackedInline): 
    model = Question
    extra = 1
    form = QuestionForm


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title','description','expire_at'] 

class AssignmentAdmin(admin.ModelAdmin):
    form = AssignmentForm
    inlines = [QuestionInline]
    list_display = ['id','title','description']

campusAdminSite.register(Assignment,AssignmentAdmin)



class SubmissionAdmin(admin.ModelAdmin):
    pass

campusAdminSite.register(Submission,SubmissionAdmin)


class QuestionAdmin(admin.ModelAdmin):

    pass

campusAdminSite.register(Question,QuestionAdmin)


# Register your models here.
