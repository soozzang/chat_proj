from django.urls import path , include,re_path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r'^ws/room_chat/(?P<name>\w+)/$', ChatConsumer.as_asgi()),
]