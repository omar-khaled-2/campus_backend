from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import QuestionList,QuestionDetail,AnswerList,QuestionVotes,AnswerVotes,QuestionSave,SavedQuestionList,DetailedAnswer

urlpatterns = [
    path('', QuestionList.as_view()),
    path('<int:pk>/', QuestionDetail.as_view()),
    path('<int:pk>/votes/', QuestionVotes.as_view()),
    path('<int:pk>/answers/', AnswerList.as_view()),
    path('<int:question_id>/answers/<int:answer_id>/votes/', AnswerVotes.as_view()),
    path('<int:question_id>/answers/<int:answer_id>/', DetailedAnswer.as_view()),
    path('<int:pk>/save/', QuestionSave.as_view()),
    path('saved/', SavedQuestionList.as_view()),

    path('<int:question_id>/answers/<int:answer_id>/votes/', AnswerVotes.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)
