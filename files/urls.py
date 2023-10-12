from django.urls import path
from .views import RootFoldersList,FilesList,NestedFoldersList,FolderAndFilesList,DetailedFile,DetailedFolder,FolderNotifications
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', RootFoldersList.as_view()),
    path('<int:pk>/files/',FilesList.as_view()),
    path('<int:folder_id>/files/<int:file_id>/',DetailedFile.as_view()),
    path('<int:pk>/folders/',NestedFoldersList.as_view()),
    path('<int:pk>/',DetailedFolder.as_view()),
    path('<int:pk>/files-folders/',FolderAndFilesList.as_view()),
    path('<int:pk>/notifications/',FolderNotifications.as_view()),


]


urlpatterns = format_suffix_patterns(urlpatterns)
