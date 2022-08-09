from rest_framework import serializers

from authentication.serializers import AccountSerializer

from .models import (
    Chat, Message
)


class ChatSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)
    participants = AccountSerializer(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = ('id', 'owner', 'name', 'participants')


class MessageSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ("id", "owner", "chat", "content", "date_added", )
