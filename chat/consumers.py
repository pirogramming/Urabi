import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from .models import ChatRoom, Message
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

# 로거 생성 (DEBUG 레벨)
logger = logging.getLogger("chat.consumer")
logger.setLevel(logging.DEBUG)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug("CONNECT 시도")
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        logger.debug(f"Room ID: {self.room_id}, Group: {self.room_group_name}")

        # 쿼리스트링에서 토큰 추출
        query_string = self.scope['query_string'].decode()
        token = ""
        if query_string:
            parts = query_string.split('=')
            if len(parts) > 1:
                token = parts[1]
        logger.debug(f"추출된 토큰: {token}")

        self.user = await self.get_user_from_token(token)
        logger.debug(f"사용자: {self.user}")

        if not await self.validate_participation():
            logger.error("참여 권한 없음 - 연결 종료")
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.debug("WebSocket 연결 수락됨 및 그룹 가입 완료")

        messages = await self.get_existing_messages()
        logger.debug(f"기존 메시지 {len(messages)}개 전송")
        await self.send(text_data=json.dumps({
            "type": "chat.history",
            "messages": messages,
        }))

    async def disconnect(self, close_code):
        logger.debug(f"DISCONNECT: {close_code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("content"):
            msg = await self.save_message(data["content"])

            event = {
                "type": "chat_message",  
                "message_id": msg.id,
                "content": msg.content,
                "sender_id": self.user.id,
                "sender_nickname": self.user.username,
                "timestamp": msg.timestamp.isoformat(),
                "profile_image_url": (
                    msg.sender.profile_image.url 
                    if getattr(msg.sender, 'profile_image', None) 
                       and msg.sender.profile_image 
                    else ""
                ),
            }
            # 브로드캐스트
            logger.debug(f"Broadcast event: {event}1")
            await self.channel_layer.group_send(self.room_group_name, event)
            logger.debug(f"Broadcast event: {event}2")



    async def chat_message(self, event):
    # "chat_message" 타입 이벤트를 수신
        logger.debug(f"chat_message 호출됨")
        await self.send(text_data=json.dumps(event))
        if event["sender_id"] != self.user.id:
            await self.mark_as_read(event["message_id"])

    @database_sync_to_async
    def get_existing_messages(self):
        room = ChatRoom.objects.get(id=self.room_id)
        messages = list(room.messages.order_by("timestamp").select_related("sender"))
        msg_list = []
        for message in messages:
            is_read = message.read_by.filter(id=self.user.id).exists()
            msg_list.append({
                "message_id": message.id,
                "content": message.content,
                "sender_id": message.sender.id,
                "sender_nickname": message.sender.username,
                "timestamp": message.timestamp.isoformat(),
                "is_read": is_read,
                "profile_image_url": (
                    message.sender.profile_image.url
                    if getattr(message.sender, 'profile_image', None)
                       and message.sender.profile_image
                    else ""
                ),
            })
        return msg_list

    @database_sync_to_async
    def validate_participation(self):
        return ChatRoom.objects.filter(Q(user1=self.user) | Q(user2=self.user), id=self.room_id).exists()

    
    @database_sync_to_async
    def save_message(self, content):
        logger.debug(f"save_message 호출됨: {content}")
        room = ChatRoom.objects.get(id=self.room_id)
        message = Message.objects.create(
            room=room, sender=self.user, content=content
        )
        message.read_by.add(self.user)
        room.update_last_message_time()

        logger.debug(f"메시지 저장 완료: {message.id}, {message.content}")
        return message

    @database_sync_to_async
    def mark_as_read(self, message_id):
        message = Message.objects.get(id=message_id)
        message.read_by.add(self.user)

    @database_sync_to_async
    def get_user_from_token(self, token):
        if not token:
            return self.scope.get("user", AnonymousUser())
        try:
            validated_token = UntypedToken(token)
            user_id = validated_token.payload.get("user_id")
            user = User.objects.get(id=user_id)
            return user
        except (InvalidToken, TokenError, User.DoesNotExist):
            return AnonymousUser()
