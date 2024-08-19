from django.urls import path
from .views import CreateChatView
from .views import CreateMessageView


app_name = 'xchat'

urlpatterns = [
    path('', CreateChatView.as_view(), name='create-chat'),
    path('<int:id>/messages/', CreateMessageView.as_view(), name='create-message'),
]
