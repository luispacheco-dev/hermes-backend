import json
from .models import Chat
from .models import Message
from xprofile.models import Profile
from .serializers import MessageModelSerializer
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

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
        self.send(text_data=json.dumps(message_json))
