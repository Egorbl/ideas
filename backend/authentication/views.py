from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

from .models import Account
from .serializers import RegistrationSerializer, AccountSerializer
from rest_framework.authtoken.views import (
    ObtainAuthToken,
)

user_model = get_user_model()


@api_view(['POST', ])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = "Successfuly registered a new user"
        data['email'] = account.email
        data['username'] = account.username
    else:
        return Response(serializer.errors, status=400)
    return Response(data)


class CustomObtainToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response_data = response.data
        current_user = Token.objects.get(key=response_data['token']).user
        response_data['username'] = current_user.username
        response_data['id'] = current_user.id
        response_data['image'] = str(current_user.profile_image)
        return Response(response_data)


@api_view(["GET", ])
def users_view(request):
    users = user_model.objects.all()
    serialized_users = AccountSerializer(users, many=True)
    return Response(serialized_users.data)


@api_view(['GET'])
def user_view(request, *args, **kwargs):
    username = kwargs.get("username")
    user = user_model.objects.filter(username=username).first()
    if not user:
        return Response({"error": "No user with this username"}, status=404)

    serialized_user = AccountSerializer(user).data
    serialized_user['is_owner'] = (request.user == user)
    return Response(serialized_user)
