from typing import Any

from django.http.request import HttpRequest
from .models import Question,Vote,Answer,Comment
from campus_admin.views import campusAdminSite
from django.contrib import admin


class QuestionAdmin(admin.ModelAdmin):
    exclude = ['viewer']
    
campusAdminSite.register(Question,QuestionAdmin)
campusAdminSite.register(Answer)