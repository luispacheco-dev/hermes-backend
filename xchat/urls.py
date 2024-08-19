from django.urls import path
from .views import MessagesView
from .views import CreateChatView
from .views import ReadMessagesView


app_name = 'xchat'

urlpatterns = [
    path('', CreateChatView.as_view(), name='create-chat'),
    path('<int:id>/messages/readed/', ReadMessagesView.as_view(), name='readed'),
    path('<int:id>/messages/', MessagesView.as_view(), name='get-create-messages'),
]
