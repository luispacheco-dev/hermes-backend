from xprofile.models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        attrs = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        profile = Profile.objects.get(user=self.user)
        attrs['profile_id'] = profile.id
        return attrs
