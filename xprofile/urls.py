from django.urls import path
from .views import ProfileByIdView
from .views import CreateUserProfileView
from .views import ProfileByIdLoggedView
from .views import GetProfileFriendRequestView
from .views import DeleteProfileFriendRequestView


app_name = 'xprofile'

urlpatterns = [
    path('<int:id>/', ProfileByIdView.as_view(), name='profile-by-id'),
    path('', CreateUserProfileView.as_view(), name='create-user-profile'),
    path('<int:id>/logged/', ProfileByIdLoggedView.as_view(), name='profile-by-id-logged'),
    path('<int:id>/friend-requests/', GetProfileFriendRequestView.as_view(), name='profile-by-id-friend-requests'),
    path('<int:p_id>/friend-requests/<int:r_id>/', DeleteProfileFriendRequestView.as_view(), name='profile-by-id-friend-requests-delete'),
]
