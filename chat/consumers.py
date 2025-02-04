# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import ChatRoom, Message
from django.db.models import Q
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # URL에서 room_id 가져오기 (정수형)
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"

        # JWT 토큰 처리: query_string에 token이 있으면 사용, 없으면 세션 사용자 사용
        try:
            query_string = self.scope['query_string'].decode()
            token = ""
            if "=" in query_string:
                token = query_string.split('=')[1]
            self.user = await self.get_user_from_token(token)
        except Exception as e:
            print(f"Token extraction error: {e}")
            await self.close()
            return

        # 참여 권한 확인: 사용자가 해당 채팅방의 user1 또는 user2인지 확인
        if not await self.validate_participation():
            await self.close()
            return

        # 그룹에 현재 채널 추가 및 연결 수락
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # 기존 메시지 내역을 클라이언트에 전송 (오름차순)
        messages = await self.get_existing_messages()
        await self.send(text_data=json.dumps({
            "type": "chat.history",
            "messages": messages,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # 'content'가 있으면 새 메시지로 처리
        if data.get("content"):
            message_content = data["content"]
            msg = await self.save_message(message_content)
            event = {
                "type": "chat.message",
                "message_id": msg.id,
                "content": msg.content,
                "sender_id": self.user.id,
                "sender_nickname": self.user.username,
                "timestamp": msg.timestamp.isoformat(),
            }
            await self.channel_layer.group_send(self.room_group_name, event)

    async def chat_message(self, event):
        # 그룹에서 받은 메시지를 클라이언트에 전송
        await self.send(text_data=json.dumps(event))
        # 만약 내가 보낸 메시지가 아니라면 읽음 처리
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
            })
        return msg_list

    @database_sync_to_async
    def validate_participation(self):
        return ChatRoom.objects.filter(
            Q(user1=self.user) | Q(user2=self.user), id=self.room_id
        ).exists()

    @database_sync_to_async
    def save_message(self, content):
        room = ChatRoom.objects.get(id=self.room_id)
        message = Message.objects.create(room=room, sender=self.user, content=content)
        message.read_by.add(self.user)  # 보낸 사람은 자동 읽음 처리
        room.update_last_message_time()
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
            UntypedToken(token)
            user = User.objects.get(id=UntypedToken(token).payload["user_id"])
            return user
        except (InvalidToken, TokenError, User.DoesNotExist):
            return AnonymousUser()
