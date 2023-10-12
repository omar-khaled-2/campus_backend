from campus_admin.views import campusAdminSite
from .models import File,Folder,Notification
from django.contrib import admin
# Register your models here.


class FolderAdmin(admin.ModelAdmin):
    pass



class FileAdmin(admin.ModelAdmin):
    pass

campusAdminSite.register(File,FileAdmin)
campusAdminSite.register(Folder,FolderAdmin)



