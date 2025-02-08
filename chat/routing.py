from django.urls import re_path
from .consumers import ChatConsumer
from .consumers import UserConsumer

websocket_urlpatterns = [
    re_path(r"^ws/chat/(?P<room_id>\d+)/$", ChatConsumer),
    re_path(r'^ws/user/(?P<user_id>\d+)/$', UserConsumer),
]