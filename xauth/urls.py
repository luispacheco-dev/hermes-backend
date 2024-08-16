from django.urls import path
from .views import CustomTokenObtainPairView


app_name = 'xauth'

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
]
