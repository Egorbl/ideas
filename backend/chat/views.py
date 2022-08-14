from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import Chat, Account, Message
from .serializers import ChatSerializer, MessageSerializer


class ChatAPIView(GenericAPIView, APIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(participants=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {}
        for key, value in request.data.items():
            data[key] = value

        participants_id = data.pop("participants", [])
        participants = self.get_accounts_by_id(participants_id)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if request.user not in participants:
            participants.append(request.user)

        serializer.save(owner=request.user, participants=participants)
        return Response(serializer.data)

    def get_accounts_by_id(self, accounts_id):
        accounts = []

        for account_id in accounts_id:
            new_account = Account.objects.filter(id=account_id).first()
            if not new_account:
                raise ValidationError({'participants': 'Invalid participant'})
            accounts.append(new_account)

        return accounts


class MessagesAPIView(GenericAPIView, APIView):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_id = kwargs.get("pk")
        chat = self.get_chat_or_error(chat_id)
        self.check_chat_permissions(chat)
        messages = self.get_messages_from_chat(chat)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        chat_id = kwargs.get("pk")
        chat = self.get_chat_or_error(chat_id)
        self.check_chat_permissions(chat)

        data = {}
        for key, value in request.data.items():
            data[key] = value
        data["chat"] = chat_id

        serializer = self.get_serializer(data=data, *args, **kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)

    def get_messages_from_chat(self, chat):
        messages = chat.messages.all()
        return messages

    def get_chat_or_error(self, chat_id):
        chat = Chat.objects.filter(id=chat_id).first()
        if not chat:
            raise ValidationError({"chat": "No chat with this id"})

        return chat

    def check_chat_permissions(self, chat):
        if self.request.user not in chat.participants.all():
            raise PermissionError(
                {"user": "User have no permissions to read this chat"})
