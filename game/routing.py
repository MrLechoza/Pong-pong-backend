from django.urls import re_path
from game.consumers import PingPongConsumer

websocket_urlpatterns = [
    re_path(r'ws/pingpong/(?P<room_name>\w+)/$', PingPongConsumer.as_asgi()),
]