from .models import Chat
from rest_framework import views
from xfriend.models import Friend
from rest_framework.response import Response
from .serializers import ChatModelSerializer


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
