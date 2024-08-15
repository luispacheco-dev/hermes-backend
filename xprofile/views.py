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
        user_profile_serializer = UserProfileSerializer(data=request.data)
        if not user_profile_serializer.is_valid():
            return Response(data=user_profile_serializer.errors, status=400)
        payload = user_profile_serializer.data
        try:
            user = CustomUser.objects.create_user(**payload['user'])
            profile = Profile.objects.create(user=user, **payload['profile'])
        except Exception as e:
            print(e)
            return Response(data={'error(s)': 'Internal Error'}, status=500)
        return Response(data=ProfileModelSerializer(profile).data, status=201)
