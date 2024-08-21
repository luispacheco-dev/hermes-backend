import json
from .models import Chat
from .models import Message
from xprofile.models import Profile
from asgiref.sync import async_to_sync
from .serializers import MessageModelSerializer
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = f"chat_{self.chat_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def save_messages(self, data):
        chat = Chat.objects.get(id=data['chat'])
        profile = Profile.objects.get(id=data['sender'])
        message = Message.objects.create(
            chat=chat,
            sender=profile,
            content=data['content']
        )
        return MessageModelSerializer(message).data

    def receive(self, text_data):
        data = json.loads(text_data)
        message_json = self.save_messages(data)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {'type': 'chat.message', 'message': message_json}
        )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))
