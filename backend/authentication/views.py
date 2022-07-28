from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import Account
from .serializers import RegistrationSerializer
from rest_framework.authtoken.views import (
    ObtainAuthToken,
)


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
        response_data['username'] = Token.objects.get(
            key=response_data['token']).user.username
        return Response(response_data)
