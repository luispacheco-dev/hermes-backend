from .models import Chat
from .models import Message
from rest_framework import views
from xfriend.models import Friend
from xprofile.models import Profile
from rest_framework.response import Response
from .serializers import ChatModelSerializer
from .serializers import MessageModelSerializer


class CreateChatView(views.APIView):
    
    def post(self, request):
        payload = request.data
        chat_serializer = ChatModelSerializer(data=payload)
        if not chat_serializer.is_valid():
            return Response(data=chat_serializer.errors, status=400)
        try:
            friend = Friend.objects.get(id=payload['friend'])
        except Friend.DoesNotExist:
            return Response(data={'error(s)': "Friend Doesn't Exist"}, status=400)
        if request.user != friend.sender.user and request.user != friend.receiver.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        if len(Chat.objects.filter(friend=friend)) != 0:
            return Response(data={'error(s)': 'Chat Already Exist'}, status=400)
        try:
            chat = Chat.objects.create(friend=friend)
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(data=ChatModelSerializer(chat).data, status=201)


class MessagesView(views.APIView):

    def post(self, request, id):
        try:
            chat = Chat.objects.get(id=id)
        except Chat.DoesNotExist:
            return Response(data={'error(s)': "Chat Doesn't Exist"}, status=400)
        payload = request.data
        message_serializer = MessageModelSerializer(data=payload)
        if not message_serializer.is_valid():
            return Response(data=message_serializer.errors, status=400)
        try:
            profile = Profile.objects.get(id=payload['sender'])
        except Profile.DoesNotExist:
            return Response(data={'error(s)': "Sender Doesn't Exist"}, status=400)
        if request.user != profile.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        if profile != chat.friend.sender and profile != chat.friend.receiver:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        try:
            payload.pop('sender')
            message = Message.objects.create(chat=chat, sender=profile, **payload)
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(data=MessageModelSerializer(message).data, status=201)

    def get(self, request, id):
        try:
            chat = Chat.objects.get(id=id)
        except Chat.DoesNotExist:
            return Response(data={'error(s)': "Chat Doesn't Exist"}, status=400)
        if request.user != chat.friend.sender.user and request.user != chat.friend.receiver.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        messages = Message.objects.filter(chat=chat)
        messages = [MessageModelSerializer(message).data for message in messages]
        return Response(data=messages, status=200)
