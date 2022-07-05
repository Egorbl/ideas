from django.urls import path
from .views import (
    IdeaAPIView, TagAPIView, IdeaDetailAPIView,
    CommentAPIView, CommentDetailAPIView, LikeAPIView
)

app_name = 'ideas_api'

urlpatterns = [
    path('tags/', TagAPIView.as_view()),
    path('ideas/', IdeaAPIView.as_view()),
    path('ideas/<str:pk>/', IdeaDetailAPIView.as_view()),
    path('ideas/<str:pk>/comments/', CommentAPIView.as_view()),
    path('comments/<str:comment_pk>/', CommentDetailAPIView.as_view()),
    path('publication/<str:pk>/likes/', LikeAPIView.as_view()),
]
