from django.http import Http404
from rest_framework.generics import ListAPIView,DestroyAPIView,ListCreateAPIView,RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.views import APIView
from django.db.models import Subquery, OuterRef,Count,Q,Exists
from django.db.models.functions import JSONObject
from .models import Question,Answer,Vote
from .serializers import QuestionSerializer,AnswerSerializer,DetailedQuestionSerilizer
import json
from academic.models import Course
import time
from pathlib import Path
from django.core.files.storage import default_storage
import uuid




class QuestionList(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user = self.request.user
        term = self.request.GET.get('term')
        course_code = self.request.GET.get('course_code')
        sort = self.request.GET.get('sort')  
        queryset = Question.objects.annotate(
            votes = Count("vote",filter=Q(vote__type="up")) - Count("vote",filter=Q(vote__type="down")),
            answer_count = Count("answer"),
            view_count = Count("viewer"),
        ).filter(title__icontains = term)
        if(course_code):
            queryset = queryset.filter(course_id = course_code)
        else:
            queryset = queryset.filter(course__in = Course.objects.filter(studentgroupcourse__student=user.student))
        queryset.order_by(sort)
        return queryset
    

   
    def post(self, request):
        title = request.data["title"]
        body = request.data['body']
        body = json.loads(body)
        course_code = request.data['course_code']
        files = request.FILES.getlist('files')
        user = request.user
        course = Course.objects.get(code = course_code)
        map = {}
        for file in files:
            filename = default_storage.save(f"{uuid.uuid4().hex}{Path(file.name).suffix}",file)
            file_url = default_storage.url(filename)
    
            map[file.name]  = file_url
        for item in body:
            if "insert" in item:
                if "image" in item["insert"]:
                    item["insert"]['image'] = map[item['insert']['image']]
                elif "audio" in item["insert"]:
                    item['insert']['audio'] = map[item['insert']['audio']]

        question = Question.objects.create(title = title,owner = user,body = json.dumps(body),course = course)
        return Response({"id":question.id},status=status.HTTP_201_CREATED)
    


class QuestionDetail(RetrieveDestroyAPIView):
    serializer_class = DetailedQuestionSerilizer

    def get_queryset(self):
        user = self.request.user
        return Question.objects.select_related('owner').annotate(
            votes = Count("vote",filter=Q(vote__type="up")) - Count("vote",filter=Q(vote__type="down")),
            user_vote = Subquery(Vote.objects.filter(question_id=OuterRef("pk"),owner = user).values("type")[:1]),
            answer_count = Count("answer"),
            view_count = Count("viewer"),
            is_saved = Exists(user.saved_questions.filter(id = OuterRef("pk"))),
        )

    
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object() 
        instance.viewer.add(user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        print(user)
        return super().destroy(request, *args, **kwargs)
    
    
class QuestionVotes(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        user = request.user
        type = request.data['type']
        Vote.objects.update_or_create(
            question_id = pk,
            owner = user,
            defaults={
                "type":type
            }
        )
        return Response(status=status.HTTP_201_CREATED)
    def delete(self, request,pk):
        user = request.user
        Vote.objects.filter(question_id = pk,owner = user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class QuestionSave(APIView):
    def post(self,request,pk):
        user = request.user
        question = Question.objects.get(pk = pk)
        user.saved_questions.add(question)
        return Response(status= status.HTTP_201_CREATED)
    def delete(self,request,pk):
        user = request.user
        question = Question.objects.get(pk = pk)
        user.saved_questions.remove(question)
        return Response(status= status.HTTP_204_NO_CONTENT)


class AnswerVotes(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,question_id,answer_id):
        user = request.user
        type = request.data['type']

        Vote.objects.update_or_create(
            answer_id = answer_id,
            owner = user,
            defaults={
                "type":type
            }
        )
        return Response(status=status.HTTP_201_CREATED)
    def delete(self, request,question_id,answer_id):
        user = request.user
        Vote.objects.filter(answer_id = answer_id,owner = user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerList(ListCreateAPIView):
    serializer_class = AnswerSerializer
    pagination_class = None
    def get_queryset(self):
        user = self.request.user
        return Answer.objects.select_related('owner').filter(question_id = self.kwargs['pk']).annotate(
            votes = Count("vote",filter=Q(vote__type="up")) - Count("vote",filter=Q(vote__type="down")),
            user_vote = Subquery(Vote.objects.filter(answer_id=OuterRef("pk"),owner = user).values("type")[:1]),
        ).order_by('created_at')

    def create(self, request,pk, *args, **kwargs):
        body = request.data['body']
        files = request.FILES.getlist('files')
        user = request.user
        body = json.loads(body)


        map = {}
        for file in files:
            filename = default_storage.save("%s/%s_%d%s" % (uuid.uuid4().hex,Path(file.name).suffix), file)
            file_url = default_storage.url(filename)
            map[file.name]  = file_url

        for item in body:
            if "insert" in item:
                if "image" in item["insert"]:
                    item["insert"]['image'] = map[item['insert']['image']]
                elif "audio" in item["insert"]:
                    item['insert']['audio'] = map[item['insert']['audio']]

        Answer.objects.create(owner = user,body = json.dumps(body),question_id = pk)

        return Response(status=status.HTTP_201_CREATED)
    

class SavedQuestionList(ListAPIView):
    serializer_class = QuestionSerializer
    def get_queryset(self):
        user = self.request.user
        return user.saved_questions.annotate(
            votes = Count("vote",filter=Q(vote__type="up")) - Count("vote",filter=Q(vote__type="down")),
            answer_count = Count("answer"),
            view_count = Count("viewer"),
        ).order_by('created_at')
    
    

class DetailedAnswer(APIView):
    def delete(self, request,question_id,answer_id):
        user = request.user
        try:
            answer = Answer.objects.get(pk = answer_id,question_id = question_id)

            if(user != answer.owner):
                raise PermissionDenied()
            answer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Answer.DoesNotExist:
            raise NotFound()


       