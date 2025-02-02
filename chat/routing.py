from django.urls import re_path
from . import consumers

# WebSocket 연결을 위한 URL 패턴 정의 (실시간 채팅 기능 구현을 위해 필요함)
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]