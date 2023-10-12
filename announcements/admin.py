from typing import Optional
from django.http.request import HttpRequest
from .models import Announcement
from campus_admin.views import campusAdminSite
from django.contrib import admin
from django import forms

# Register your models here.


class AnnouncementForm(forms.ModelForm):
    
    class Meta:
        model = Announcement
   
        exclude = []

    # attachments = forms.MultipleChoiceField(Attachment.objects.all())

class AnnouncementAdmin(admin.ModelAdmin):
    readonly_fields = ['owner']
    form = AnnouncementForm
    search_fields = ['text']
    list_display = ['id','owner','created_at']
    def save_model(self, request, obj, form, change):
        if not change:  # Only set owner for new instances
            obj.owner = request.user
        super().save_model(request, obj, form, change)



    def has_delete_permission(self,request,obj=None):
        if obj == None:
            return None
        user = request.user
        if user.has_perm("announcements.delete_announcement"):
            return True
        if user.has_perm("announcements.delete_own_announcement") and obj.owner == user:
            return True
            
        return False
    
    def has_change_permission(self, request: HttpRequest, obj = None) -> bool:
        if obj == None:
            return None
        user = request.user
        if user.has_perm("announcements.change_announcement"):
            return True
        if user.has_perm("announcements.change_own_announcement") and obj.owner == user:
            return True
            
        return False
    
    

    


campusAdminSite.register(Announcement,AnnouncementAdmin)