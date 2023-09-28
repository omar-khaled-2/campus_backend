from rest_framework import serializers
from academic.models import Course
from .models import Folder



class FileSerilizer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    url = serializers.FileField()
    size = serializers.IntegerField()
    created_at = serializers.DateField()


class FolderSerilizer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    created_at = serializers.DateField()
    file_count = serializers.IntegerField(default = 0)




class CreateRootFolderSerilizer(serializers.Serializer):
    name = serializers.CharField(max_length = 20)
    course_code = serializers.CharField()


    def create(self):
        name = self.validated_data['name']
        course_code = self.validated_data['course_code']
        course = Course.objects.get(code = course_code)
        folder = Folder.objects.create(name = name,course = course)
        serilizer = FolderSerilizer(folder)
        return serilizer.data
    


class CreateNestedFolderSerilizer(serializers.Serializer):
    name = serializers.CharField(max_length = 20)


