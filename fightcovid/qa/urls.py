from django.urls import path, reverse_lazy
from . import views

app_name='qa'

# delete or update option left for the future work

urlpatterns = [
    path('', views.QuestionList.as_view(), name='all'),
    path('question/<int:pk>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('question/create/', views.QuestionCreate.as_view(success_url = reverse_lazy('qa:all')), name='question_create'),
    path('question/<int:pk>/update', views.QuestionUpdate.as_view(), name='question_update'),
    path('question/<int:question_id>/answer', views.AnswerCreate.as_view(), name='answer_create'),
    path('vote/answer/<int:pk>', views.AnswerVoteView.as_view(), name='answer_vote'),
]
