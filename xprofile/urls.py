from django.urls import path
from .views import ProfileByIdView
from .views import CreateUserProfileView


app_name = 'xprofile'

urlpatterns = [
    path('<int:id>/', ProfileByIdView.as_view(), name='profile-by-id'),
    path('', CreateUserProfileView.as_view(), name='create-user-profile'),
]
