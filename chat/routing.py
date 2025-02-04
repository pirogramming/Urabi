# chat/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # room_id는 정수형으로 받음
    re_path(r"ws/chat/(?P<room_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
]
