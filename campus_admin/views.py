from django.contrib.admin.sites import AdminSite
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext_lazy
import boto3
from django.conf import settings
import json

class CampusAdminSite(AdminSite):
    site_title = gettext_lazy("Campus admin")
    site_header = gettext_lazy("Campus administration")

    
    
    



campusAdminSite = CampusAdminSite()

