from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import Account
from .serializers import RegistrationSerializer


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
        data = serializer.errors
    return Response(data)
