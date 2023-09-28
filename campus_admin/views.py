from django.contrib.admin.sites import AdminSite
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext_lazy
import boto3
from django.conf import settings
import json

class CampusAdminSite(AdminSite):
    site_title = gettext_lazy("Campus amin")
    site_header = gettext_lazy("Campus administration")

    


    def has_permission(self, request):
        user = request.user
        return user.has_perm("admin.can_access_admin_site")
    
    



campusAdminSite = CampusAdminSite()

