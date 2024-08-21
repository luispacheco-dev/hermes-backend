from .models import Friend
from django.db.models import Q
from rest_framework import views
from .models import FriendRequest
from xprofile.models import Profile
from rest_framework.response import Response
from .serializers import FriendModelSerializer
from .serializers import FriendRequestModelSerializer


class CreateFriendRequestView(views.APIView):

    def post(self, request):
        payload = request.data
        friend_request_serializer = FriendRequestModelSerializer(data=payload)
        if not friend_request_serializer.is_valid():
            return Response(data=friend_request_serializer.errors, status=400)
        try:
            profile = Profile.objects.get(id=payload['sender'])
        except Profile.DoesNotExist:
            return Response(data={'error(s)': "Profile Doesn't Exist"}, status=400)
        if request.user != profile.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        try:
            receiver_profile = Profile.objects.get(code=payload['code'])
        except Profile.DoesNotExist:
            return Response(data={'error(s)': "Code Doesn't Exist"}, status=400)
        if len(FriendRequest.objects.filter(sender=profile, code=payload['code'])) != 0:
            return Response(data={'error(s)': 'Friend Request Already Exist'}, status=400)
        if len(FriendRequest.objects.filter(sender=receiver_profile, code=profile.code)) != 0:
            return Response(data={'error(s)': 'Friend Request Already Exist'}, status=400)
        try:
            payload.pop('sender')
            friend_request = FriendRequest.objects.create(sender=profile, **payload)
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(data=FriendRequestModelSerializer(friend_request).data, status=201)


class CreateFriendView(views.APIView):

    def post(self, request):
        payload = request.data
        friend_serializer = FriendModelSerializer(data=payload)
        if not friend_serializer.is_valid():
            return Response(data=friend_serializer.errors, status=400)
        try:
            receiver_profile = Profile.objects.get(id=payload['receiver'])
        except Profile.DoesNotExist:
            return Response(data={'error(s)': "Receiver Profile Doesn't Exist"}, status=400)
        if request.user != receiver_profile.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        try:
            sender_profile = Profile.objects.get(id=payload['sender'])
        except Profile.DoesNotExist:
            return Response(data={'error(s)': "Sender Profile Doesn't Exist"}, status=400)
        if len(FriendRequest.objects.filter(sender=sender_profile, code=receiver_profile.code)) == 0:
            return Response(data={'error(s)': "Friend Request Doesn't Exist"}, status=400)
        if len(Friend.objects.filter(sender=sender_profile, receiver=receiver_profile)) != 0:
            return Response(data={'error(s)': 'Friend Already Exist'}, status=400)
        try:
            friend = Friend.objects.create(sender=sender_profile, receiver=receiver_profile)
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        try:
            FriendRequest.objects.get(sender=sender_profile, code=receiver_profile.code).delete()
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(data=FriendModelSerializer(friend).data, status=201)


class DeleteFriendView(views.APIView):

    def delete(self, request, id):
        try:
            friend = Friend.objects.get(id=id)
        except Friend.DoesNotExist:
            return Response(data={'error(s)': "Friend Doesn't Exist"}, status=400)
        if request.user != friend.sender.user and request.user != friend.receiver.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        friend_request = FriendRequest.objects.filter(
            Q(sender=friend.sender, code=friend.receiver.code) |
            Q(sender=friend.receiver, code=friend.sender.code)
        ).first()
        try:
            friend.delete()
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(status=200)
