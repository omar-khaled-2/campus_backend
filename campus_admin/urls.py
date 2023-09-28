from django.urls import path
from .views import campusAdminSite

urlpatterns = [
    path('', campusAdminSite.urls),
]
