from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import AnnouncementSerializer,CreateAnnouncmentSerilizer
from .models import Announcement,Reaction
from django.db.models import Count,Q,Subquery,OuterRef,Exists
from rest_framework import status
from academic.models import Course
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied


class AnnouncementList(ListAPIView):
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        user = self.request.user

        search_term = self.request.GET.get('search_term')
        queryset = Announcement.objects.annotate(
            like_count = Count('reaction', filter=Q(reaction__type='like')),
            dislike_count = Count('reaction', filter=Q(reaction__type='dislike')),
            user_reaction = Subquery(
                Reaction.objects.filter(
                    announcement=OuterRef('pk'),
                    user=user
                ).values('type')[:1]
            ),
            is_saved = Exists(
                user.saved_announcements.filter(pk=OuterRef('pk'))
            )
        ).filter(course__in = Course.objects.filter(studentgroupcourse__student__user=user)).order_by('-created_at')

        if search_term != "":
            queryset = queryset.filter(text__icontains = search_term)
        
        return queryset
    
    def post(self,request):
        user = request.user
        if not user.has_perm("announcements.add_announcement"):
            raise PermissionDenied()
        serilizer = CreateAnnouncmentSerilizer(data= request.data)
        serilizer.is_valid(raise_exception=True)

        text = serilizer.validated_data.get("text")
        image = serilizer.validated_data.get("image")
        course_code = serilizer.validated_data.get("course_code")
        user.announcement_set.create(course_id = course_code, text = text, image = image)

        return Response(status=status.HTTP_201_CREATED)
    

 
class AnnouncementReaction(APIView):
  
    def post(self,request,pk):
        user = request.user
        if not user.has_perm('announcements.react_annoucements'):
            raise PermissionDenied()
        type = request.data['type']
        Reaction.objects.update_or_create(
            announcement_id = pk,
            user = user,
            defaults={
                "type":type
            }
        )
        return Response(status=status.HTTP_201_CREATED)
    def delete(self, request,pk):
        user = request.user
        Reaction.objects.filter(announcement_id = pk,user = user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class SavedAnnouncementList(ListAPIView):
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = user.saved_announcements.annotate(
            like_count = Count('reaction', filter=Q(reaction__type='like')),
            dislike_count = Count('reaction', filter=Q(reaction__type='dislike')),
            user_reaction = Subquery(
                Reaction.objects.filter(
                    announcement=OuterRef('pk'),
                    user=user
                ).values('type')[:1]
            ),
            is_saved = Exists(
                user.saved_announcements.filter(pk=OuterRef('pk'))
            )
        )
        
        return queryset
    
class DetailAnnouncement(APIView):
    def delete(self, request,pk):
        user = request.user
        if not user.has_perm('announcements.delete_announcement'):
            raise PermissionDenied()
        Announcement.objects.filter(pk = pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AnnouncementSave(APIView):
    def post(self,request,pk):
        user = request.user
        announcement = Announcement.objects.get(pk = pk)
        user.saved_announcements.add(announcement)
        return Response(status= status.HTTP_201_CREATED)
    def delete(self,request,pk):
        user = request.user
        announcement = Announcement.objects.get(pk = pk)
        user.saved_announcements.remove(announcement)
        return Response(status= status.HTTP_204_NO_CONTENT)