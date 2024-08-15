from django.urls import path
from .views import CreateUserProfileView


app_name = 'xprofile'

urlpatterns = [
    path('', CreateUserProfileView.as_view(), name='create-user-profile'),
]
