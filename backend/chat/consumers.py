from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from asgiref.sync import async_to_sync
import json
import uuid
from django.conf import settings

from .models import Message
from .serializers import MessageSerializer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.group_name = chat_id
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        data = self.save(message)
        data_bytes = JSONRenderer().render(data)
        data_dict = data_bytes.decode('UTF-8')
        data_dict = json.loads(data_dict)
        data_dict['type'] = 'chat_message'

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            data_dict
        )

    def save(self, message):
        token = self.scope['query_string'].decode('UTF-8')
        owner = Token.objects.filter(key=token).first().user
        chat = self.group_name
        dataToPost = {
            "id": str(uuid.uuid4()),
            "chat": chat,
            "content": message
        }
        serializer = MessageSerializer(data=dataToPost)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=owner)
        return serializer.data

    def chat_message(self, event):
        print(event)
        self.send(text_data=json.dumps(event))
