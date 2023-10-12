from typing import Any, Tuple
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import User,Student,Teacher,Device,StudentGroupCourse
from campus_admin.views import campusAdminSite
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    exclude = ['password',"last_login"]
    list_display = ['id','first_name','last_name']
    search_fields = ['id']

    
    



campusAdminSite.register(User,UserAdmin)
campusAdminSite.register(Student)
campusAdminSite.register(Teacher)
campusAdminSite.register(Group)
campusAdminSite.register(Permission)
campusAdminSite.register(Device)
campusAdminSite.register(StudentGroupCourse)


