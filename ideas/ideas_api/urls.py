from django.urls import path
from .views import (
    IdeaAPIView, TagAPIView, IdeaDetailAPIView,
    CommentAPIView, CommentDetailAPIView, LikeAPIView, LikeDetailAPIView
)

app_name = 'ideas_api'

urlpatterns = [
    path('tags/', TagAPIView.as_view()),  # GET
    path('ideas/', IdeaAPIView.as_view()),  # GET
    path('ideas/<str:pk>/', IdeaDetailAPIView.as_view()),  # GET
    path('ideas/<str:pk>/comments/', CommentAPIView.as_view()),  # GET
    path('comments/<str:comment_pk>/',
         CommentDetailAPIView.as_view()),  # GET
    path('publication/<str:pk>/likes/', LikeAPIView.as_view()),  # GET
    path('likes/<str:pk>/', LikeDetailAPIView.as_view()),
]
