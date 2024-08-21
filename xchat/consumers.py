import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        text_data_json = json.load(text_data)
        content = text_data_json['content']
        self.send(text_data=json.dump({'content': content}))
