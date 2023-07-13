import os
import django
from channels.routing import get_default_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_proj.settings')

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing

django.setup()
application = get_default_application()


# application = ProtocolTypeRouter(
#     {
#         "http" : get_asgi_application() ,
#         "websocket" : AuthMiddlewareStack(
#             URLRouter(
#                 routing.websocket_urlpatterns
#             )   
#         )
#     }
# )