from django.urls import path , include,re_path
from .consumers import ChatConsumer


websocket_urlpatterns = [
	path("<room_id>" , ChatConsumer.as_asgi()) ,
    re_path(r'^wss/(?P<room_id>[^/]+)/$', ChatConsumer.as_asgi()),
]