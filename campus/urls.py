from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('api/announcements/',include("announcements.urls")),
    path('api/questions/',include("questions.urls")),
    path('api/',include("academic.urls")),
    path('api/folders/',include("files.urls")),
    path('api/',include("user.urls")),
    path('admin/', include("campus_admin.urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

