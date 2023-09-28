from rest_framework import serializers
from .models import Course
from user.models import Teacher


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class DetailedLocationSerilizer(LocationSerializer):
    building = serializers.CharField()
    floor = serializers.IntegerField()
    description = serializers.CharField()

class CourseSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField(source = "english_name")


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    # is_enrolled = serializers.BooleanField()

class CourseWithGroupsSerializer(CourseSerializer):
    enrolled_group_id = serializers.IntegerField(allow_null = True)

    groups = serializers.ListSerializer(child = GroupSerializer(),source = 'group_set')
    


class TeacherSerilizer(serializers.Serializer):
    name = serializers.CharField()
    title = serializers.ChoiceField(choices=Teacher.Title)


class ActivitySerializer(serializers.Serializer):

    type = serializers.CharField()
    course = serializers.CharField()
    instructor = TeacherSerilizer()



class ScheduleSerializer(serializers.Serializer):
    activity = ActivitySerializer()
    start_at = serializers.TimeField()
    end_at = serializers.TimeField()
    location = LocationSerializer()


