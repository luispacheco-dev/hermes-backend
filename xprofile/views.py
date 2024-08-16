from .models import Profile
from .models import CustomUser
from django.db.models import Q
from rest_framework import views
from xfriend.models import Friend
from xfriend.models import FriendRequest
from rest_framework.response import Response
from .serializers import UserProfileSerializer
from .serializers import ProfileModelSerializer
from rest_framework.permissions import AllowAny


class CreateUserProfileView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.data
        user_profile_serializer = UserProfileSerializer(data=payload)
        if not user_profile_serializer.is_valid():
            return Response(data=user_profile_serializer.errors, status=400)
        try:
            user = CustomUser.objects.create_user(**payload['user'])
            profile = Profile.objects.create(user=user, **payload['profile'])
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(data=ProfileModelSerializer(profile).data, status=201)


class ProfileByIdView(views.APIView):

    def get(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(data={'error(s)': "Profile Doesn't Exist"}, status=400)
        return Response(data=ProfileModelSerializer(profile).data, status=200)

    def delete(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except:
            return Response(data={'error(s)': "Profile Doesn't Exist"}, status=400)
        if request.user != profile.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        try:
            request.user.delete()
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(status=200)

    def patch(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except:
            return Response(data={'error(s)': "Profile Doesn't Exist"}, status=400)
        if request.user != profile.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        payload = request.data
        profile_serializer = ProfileModelSerializer(data=payload)
        if not profile_serializer.is_valid():
            return Response(data=profile_serializer.errors, status=400)
        profile.last_name = payload['last_name']
        profile.first_name = payload['first_name']
        profile.picture = profile.picture if 'picture' not in payload else payload['picture']
        profile.save()
        return Response(data=ProfileModelSerializer(profile).data, status=200)


class ProfileByIdLoggedView(views.APIView):

    def patch(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except:
            return Response(data={'error(s)': "Profile Doesn't Exist"}, status=400)
        if request.user != profile.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        payload = request.data
        if 'logged' not in payload or type(payload['logged']) is not bool:
            return Response(data={'error(s)': 'Logged Field Is Required (Bool)'}, status=400)
        profile.logged = payload['logged']
        profile.save()
        return Response(data={'logged': payload['logged']}, status=200)


class GetProfileFriendRequestView(views.APIView):

    def get(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(data={'error(s)': "Profile Doesn't Exist"}, status=400)
        if request.user != profile.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        friend_request_serializers = []
        friend_requests = FriendRequest.objects.filter(code=profile.code)
        for friend_request in friend_requests:
            friend_request_serializer = dict()
            friend_request_serializer['id'] = friend_request.id
            friend_request_serializer['requested_at'] = friend_request.requested_at
            friend_request_serializer['profile'] = ProfileModelSerializer(friend_request.sender).data
            friend_request_serializers.append(friend_request_serializer)
        return Response(data=friend_request_serializers, status=200)


class DeleteProfileFriendRequestView(views.APIView):

    def delete(self, request, p_id, r_id):
        try:
            profile = Profile.objects.get(id=p_id)
        except Profile.DoesNotExist:
            return Response(data={'error(s)': "Profile Doesn't Exist"}, status=400)
        if request.user != profile.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        try:
            friend_request = FriendRequest.objects.get(id=r_id)
        except FriendRequest.DoesNotExist:
            return Response(data={'error(s)': "Friend Request Doesn't Exist"})
        try:
            friend_request.delete()
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(status=200)


class GetProfileFriends(views.APIView):

    def get(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(data={'error(s)': "Profile Doesn't Exist"}, status=400)
        if request.user != profile.user:
            return Response(data={'error(s)': 'Forbidden Resource'}, status=403)
        friend_serializers = []
        friends = Friend.objects.filter(Q(sender=profile) | Q(receiver=profile))
        for friend in friends:
            friend_serializer = dict()
            friend_serializer['id'] = friend.id
            friend_serializer['began_at'] = friend.began_at
            profile_ = friend.sender if profile != friend.sender else friend.receiver
            friend_serializer['profile'] = ProfileModelSerializer(profile_).data
            friend_serializers.append(friend_serializer)
        return Response(data=friend_serializers, status=200)
