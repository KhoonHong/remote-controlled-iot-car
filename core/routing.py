# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from apps.home import consumers  # Adjust this import to your project structure

websocket_urlpatterns = [
    path('ws/motion/', consumers.MotionConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
