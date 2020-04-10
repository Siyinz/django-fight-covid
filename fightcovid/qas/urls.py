from django.urls import path, reverse_lazy
from . import views

app_name='qas'

# delete or update option left for the future work

urlpatterns = [
    path('', views.QuestionList.as_view(), name='all'),
    path('question/<int:pk>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('question/create/', views.QuestionCreate.as_view(success_url = reverse_lazy('qas:all')), name='question_create'),
#    path('question/<int:pk>/update', views.QuestionUpdate.as_view(success_url = reverse_lazy('qas:all')), name='question_update'),
#    path('question/<int:pk>/delete', views.QuestionDelete.as_view(success_url = reverse_lazy('qas:all')), name='question_delete'),
    path('question/<int:question_id>/answer', views.AnswerCreate.as_view(), name='answer_create'),
    path('question/<int:pk>/tag', views.TagCreate.as_view(), name='question_tag_create'),
#    path('tag/<int:pk>/delete', views.TagDelete.as_view(success_url = reverse_lazy('qas')), name='question_tag_delete'),
]
