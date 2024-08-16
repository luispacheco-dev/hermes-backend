from .models import Profile
from .models import CustomUser
from rest_framework import views
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
