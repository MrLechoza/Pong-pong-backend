from django.urls import path
from game.consumers import PingPongConsumer

websocket_urlpatterns = [
    path('ws/pingpong/', PingPongConsumer.as_asgi()),
]