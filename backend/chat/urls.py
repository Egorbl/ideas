from django.urls import path

from .views import (
    ChatAPIView, MessagesAPIView,
)

urlpatterns = [
    path("chats/", ChatAPIView.as_view()),  # GET, POST
    path("chats/<str:pk>/messages/", MessagesAPIView.as_view()),   # GET, POST
]
