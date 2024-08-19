from django.urls import path
from .views import CreateChatView


app_name = 'xchat'

urlpatterns = [
    path('', CreateChatView.as_view(), name='create-chat'),
]
