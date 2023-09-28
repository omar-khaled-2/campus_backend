from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import AnnouncementList,AnnouncementReaction,AnnouncementSave,SavedAnnouncementList,DetailAnnoncement

urlpatterns = [
    path('', AnnouncementList.as_view()),
    path('saved/', SavedAnnouncementList.as_view()),
    path('<int:pk>/reactions/', AnnouncementReaction.as_view()),
    path('<int:pk>/save/', AnnouncementSave.as_view()),
    path('<int:pk>/', DetailAnnoncement.as_view())


]

urlpatterns = format_suffix_patterns(urlpatterns)
