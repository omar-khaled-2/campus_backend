from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .models import Course,Schedule,Location,Group
from .serializers import CourseSerializer,ScheduleSerializer,DetailedLocationSerilizer,CourseWithGroupsSerializer
from django.db.models import F,Exists,OuterRef,Subquery
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user.models import Student,StudentGroupCourse

class CourseList(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = None
    
    def get_queryset(self):
        user = self.request.user
        return Course.objects.prefetch_related("group_set").annotate(
            enrolled_group_id = Subquery(StudentGroupCourse.objects.filter(course__code = OuterRef("code"),student = user.student).values("group_id")[:1])
        )
    

    serializer_class = CourseWithGroupsSerializer


class ScheduleList(APIView):
 

    def get(self,request):
        user = request.user
        date  = self.request.query_params.get('date')
        schedules = Schedule.objects.annotate(
            start_at = F('start_period__start_at'),
            end_at =  F('end_period__end_at')

        ).filter(date = date,groups__in = Group.objects.filter(studentgroupcourse__student = user.student))
        serilizer = ScheduleSerializer(schedules,many = True)

        
        return Response(serilizer.data)
    
class DetailedLocation(RetrieveAPIView):
    queryset = Location.objects
    serializer_class = DetailedLocationSerilizer
    