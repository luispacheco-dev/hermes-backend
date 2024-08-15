from .models import Profile
from .models import CustomUser
from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class ProfileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ['user']
        read_only_fields = ['code', 'username', 'last_login', 'created_at']


class UserProfileSerializer(serializers.Serializer):
    user = UserModelSerializer()
    profile = ProfileModelSerializer()
