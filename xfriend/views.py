from rest_framework import views
from .models import FriendRequest
from xprofile.models import Profile
from rest_framework.response import Response
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
        if len(Profile.objects.filter(code=payload['code'])) == 0:
            return Response(data={'error(s)': "Code Doesn't Exist"}, status=400)
        if len(FriendRequest.objects.filter(sender=profile, code=payload['code'])) != 0:
            return Response(data={'error(s)': 'Friend Request Already Exist'}, status=400)
        try:
            payload.pop('sender')
            friend_request = FriendRequest.objects.create(sender=profile, **payload)
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(data=FriendRequestModelSerializer(friend_request).data, status=201)
