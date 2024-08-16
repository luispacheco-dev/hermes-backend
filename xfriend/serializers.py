from rest_framework import serializers
from .models import Friend, FriendRequest


class FriendModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Friend
        fields = '__all__'
        read_only_fields = ['began_at']


class FriendRequestModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = '__all__'
        read_only_fields = ['requested_at']
