from django.urls import path
from rest_framework.authtoken.views import (
    obtain_auth_token,
)
from .views import (
    registration_view, CustomObtainToken, users_view, user_view, user_update_view, change_password_view
)

app_name = 'authentication'

urlpatterns = [
    path('login/', CustomObtainToken.as_view()),
    path('register/', registration_view),
    path('users/', users_view),
    path('users/<str:username>/', user_view),
    path('update_user/<str:id>/', user_update_view),
    path('change_password/<str:id>/', change_password_view),
]
