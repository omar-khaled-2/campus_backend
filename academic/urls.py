from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CourseList,ScheduleList,DetailedLocation

urlpatterns = [
    path('courses/', CourseList.as_view()),
    path("schedules/",ScheduleList.as_view()),
    path('locations/<int:pk>/',DetailedLocation.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)
