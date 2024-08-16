from django.urls import path
from .views import CreateFriendRequestView


app_name = 'xfriend'

urlpatterns = [
    path('friend-requests/', CreateFriendRequestView.as_view(), name='friend-requests'),
]
