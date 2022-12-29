# routing.py

# routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})


