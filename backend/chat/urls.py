from django.urls import path

from .views import main_chat_page, room_page

app_name = 'chat'

urlpatterns = [
    path('', main_chat_page),
    path('<str:room_name>', room_page),
]
