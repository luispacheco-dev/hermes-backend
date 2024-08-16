from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'xauth'

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
