from django.urls import path
from .views import RootFoldersList,FilesList,NestedFoldersList,FolderAndFilesList,DetailFile
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', RootFoldersList.as_view()),
    path('<int:pk>/files/',FilesList.as_view()),
    path('<int:folder_id>/files/<int:file_id>/',DetailFile.as_view()),
    path('<int:pk>/folders/',NestedFoldersList.as_view()),
    path('<int:pk>/',FolderAndFilesList.as_view())


]


urlpatterns = format_suffix_patterns(urlpatterns)
