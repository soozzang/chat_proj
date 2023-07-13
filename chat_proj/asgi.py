import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from chats.routing import websocket_urlpatterns
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_proj.settings")
django.setup()
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# from .consumers import ChatConsumer

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)



# import os
# import django
# from channels.routing import get_default_application


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_proj.settings')

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from . import routing

# django.setup()
# application = get_default_application()


# # application = ProtocolTypeRouter(
# #     {
# #         "http" : get_asgi_application() ,
# #         "websocket" : AuthMiddlewareStack(
# #             URLRouter(
# #                 routing.websocket_urlpatterns
# #             )   
# #         )
# #     }
# # )