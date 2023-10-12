from rest_framework import serializers
from .models import Question,Answer
from user.serializers import UserSerializer
from academic.serializers import CourseSerializer


class CreateQuestionSerilizer(serializers.Serializer):
    title = serializers.CharField(min_length = 20,max_length = 200)
    body = serializers.CharField(min_length = 10)


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    owner = UserSerializer()
    votes = serializers.IntegerField()
    answer_count = serializers.IntegerField()
    view_count = serializers.IntegerField()
    course = CourseSerializer()
    created_at = serializers.DateTimeField()


class DetailedQuestionSerilizer(QuestionSerializer):
    body = serializers.CharField()
    user_vote = serializers.CharField(allow_null = True)
    is_saved = serializers.BooleanField()
    is_notifications_active = serializers.BooleanField()

class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    owner = UserSerializer()
    body = serializers.CharField()
    votes = serializers.IntegerField(default = 0)
    user_vote = serializers.CharField(allow_null = True)

    