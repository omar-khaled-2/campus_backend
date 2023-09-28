from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.views import APIView
from .serializers import FileSerilizer,FolderSerilizer,CreateRootFolderSerilizer,CreateNestedFolderSerilizer
from .models import File,Folder
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound,PermissionDenied

from academic.models import Course
from django.db.models import Count
from rest_framework.exceptions import APIException
from rest_framework.permissions import DjangoModelPermissions

class FilesList(APIView):

    def post(self,request,pk):
        f = request.data['file']
        file = File.objects.create(folder_id = pk,url = f,name = f.name)
        serilizer = FileSerilizer(file)
        
        return Response(serilizer.data,status=status.HTTP_201_CREATED)
    

class DetailFile(APIView):
    def delete(self,request,folder_id,file_id):
        user = request.user


        if not user.has_perm('files.delete_file'):
            raise PermissionDenied(detail="you don't have permission to delete this file")
        try:
            file = File.objects.get(folder_id = folder_id,pk = file_id)
            file.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except File.DoesNotExist:
            raise NotFound("File does not exist")

class RootFoldersList(ListAPIView):
    serializer_class = FolderSerilizer
    pagination_class = None
    def get_queryset(self):
        course_code = self.request.GET.get('course_code')
        return Folder.objects.filter(course__code = course_code).annotate(
            file_count = Count("file")
        ).order_by("created_at")

    def post(self,request):
        serilizer = CreateRootFolderSerilizer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        folder = serilizer.create()
        return Response(folder,status=status.HTTP_201_CREATED)
        
        
class NestedFoldersList(CreateAPIView):
    
    def create(self, request, pk):

        serilizer = CreateNestedFolderSerilizer(data=request.data)
        serilizer.is_valid(raise_exception=True)

        name = serilizer.validated_data['name']
        parent = Folder.objects.get(pk = pk)
        folder = Folder.objects.create(name = name,parent = parent)
        serilizer = FolderSerilizer(folder)
        return Response(serilizer.data,status=status.HTTP_201_CREATED)
        

        
class FolderAndFilesList(APIView):
    def get(self, request, pk):
        user = request.user
        
        parent = Folder.objects.get(pk = pk)
        folders = Folder.objects.filter(parent = parent).order_by("created_at")
        files = File.objects.filter(folder = parent).order_by("created_at")
        return Response({
            "folders": FolderSerilizer(folders,many=True).data,
            "files": FileSerilizer(files,many=True).data
        })