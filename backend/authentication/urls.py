from django.urls import path
from rest_framework.authtoken.views import (
    obtain_auth_token,
)
from .views import (
    registration_view, CustomObtainToken
)

app_name = 'authentication'

urlpatterns = [
    path('login/', CustomObtainToken.as_view()),
    path('register/', registration_view),
]
