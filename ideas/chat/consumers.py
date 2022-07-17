from cgitb import text
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = 'chat_%s' % room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data.get('message')

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'send_message',
                'message': message,
            }
        )

    def send_message(self, text_data=None):
        json_data = json.dumps(text_data)
        self.send(json_data)
