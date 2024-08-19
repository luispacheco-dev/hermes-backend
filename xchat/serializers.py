from .models import Chat
from .models import Message
from rest_framework import serializers


class ChatModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chat
        fields = '__all__'


class MessageModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['readed', 'created_at', 'chat']
