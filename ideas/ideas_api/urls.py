from django.urls import path
from .views import (
    IdeaAPIView, TagAPIView, IdeaDetailAPIView, CommentAPIView,
)

app_name = 'ideas_api'

urlpatterns = [
    path('ideas/', IdeaAPIView.as_view()),
    path('ideas/<str:pk>/', IdeaDetailAPIView.as_view()),
    path('ideas/<str:pk>/comments/', CommentAPIView.as_view()),
    #  ideas/<str:pk>/comments/<str:pk>/ DELETE, UPDATE, RETRIEVE + was liked field
    path('tags/', TagAPIView.as_view()),  # GET, POST
    #  ideas/<str:pk>/likes/ POST DELETE
]
