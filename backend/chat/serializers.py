from rest_framework import serializers

from authentication.serializers import AccountSerializer

from .models import (
    Chat, Message
)


class ChatSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)
    participants = AccountSerializer(read_only=True, many=True)
    last_message = serializers.SerializerMethodField(
        read_only=True, method_name="get_last_message")

    class Meta:
        model = Chat
        fields = ('id', 'owner', 'name', 'participants', 'last_message')

    def get_last_message(self, obj):
        message = obj.messages.all().order_by('-date_added').first()
        if message:
            message = MessageSerializer(message).data

        return message


class MessageSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField(
        read_only=True, method_name="get_is_owner")

    class Meta:
        model = Message
        fields = ("id", "owner", "chat", "content", "date_added", "is_owner")

    def get_is_owner(self, obj):
        return True
        # if not self.context['request'].user.is_authenticated:
        #     return False

        # idea_owner = obj.owner
        # return True if idea_owner == self.context['request'].user else False
