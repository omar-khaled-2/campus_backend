from typing import Optional
from django.http.request import HttpRequest
from .models import Course,CourseGPA,Schedule,Activity,Group,Period,Location
from campus_admin.views import campusAdminSite
from django.contrib import admin
from django import forms


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class GroupInline(admin.TabularInline):
    model = Group
    form = GroupForm
    
    






class CourseAdmin(admin.ModelAdmin):
    actions_selection_counter = False
    fields = ['code',('arabic_name',"english_name"),"prerequisite","credit_hours"]
    list_display = ['code','arabic_name',"english_name","credit_hours"]
    search_fields = ['code','arabic_name',"english_name"]
    search_help_text = "Search by code , arabic name or english name"
 
    inlines = [GroupInline]
    pass


campusAdminSite.register(Course,CourseAdmin)


class ScheduleForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects)

    class Meta:
        model = Schedule
        fields = 'start_period','end_period','date',"groups",'location'



class ScheduleInline(admin.StackedInline):
    model = Schedule
    extra = 1
    form = ScheduleForm


    
    

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'  # Or specify the fields you want to display in the form


class ActivityAdmin(admin.ModelAdmin):
    form = ActivityForm
    inlines = [ScheduleInline]

    def has_view_permission(self, request: HttpRequest, obj = None) -> bool:
        return True



campusAdminSite.register(Activity,ActivityAdmin)



class PeriodAdmin(admin.ModelAdmin):
    list_display = ['id','start_at','end_at']
    ordering = ['id']

campusAdminSite.register(Period,PeriodAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']

campusAdminSite.register(Location,LocationAdmin)


campusAdminSite.register(Schedule)