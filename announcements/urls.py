from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import AnnouncementList,AnnouncementReaction,AnnouncementSave,SavedAnnouncementList,DetailAnnouncement

urlpatterns = [
    path('', AnnouncementList.as_view()),
    path('saved/', SavedAnnouncementList.as_view()),
    path('<int:pk>/reactions/', AnnouncementReaction.as_view()),
    path('<int:pk>/save/', AnnouncementSave.as_view()),
    path('<int:pk>/', DetailAnnouncement.as_view())


]

urlpatterns = format_suffix_patterns(urlpatterns)
