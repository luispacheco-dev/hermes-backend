from django.urls import path
from .views import CreateFriendView
from .views import CreateFriendRequestView


app_name = 'xfriend'

urlpatterns = [
    path('', CreateFriendView.as_view(), name='create-friend'),
    path('friend-requests/', CreateFriendRequestView.as_view(), name='friend-requests'),
]
