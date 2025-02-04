import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from .models import ChatRoom, Message
from users.models import User
from django.db.models import Q

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        웹소켓 연결 처리:
          - JWT 토큰 기반 사용자 인증
          - 채팅방 참여 여부 확인 후 그룹에 추가
          - 기존 메시지 전송
        """
        self.room_id = self.scope['url_route']['kwargs']['room_id']  # 채팅방 ID
        self.room_group_name = f'chat_{self.room_id}'  # 그룹 이름

        # JWT 토큰 기반 사용자 인증
        try:
            query_string = self.scope['query_string'].decode()
            token = query_string.split('=')[1] if '=' in query_string else ''
            print(f"Received token: {token}")
            self.user = await self.get_user_from_token(token)
        except Exception as e:
            print(f"Error during token extraction: {e}")
            await self.close()
            return

        # 채팅방 참여 여부 확인
        if await self.validate_participation():
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()
    
    async def receive(self, text_data):
        """
        클라이언트로부터 메시지 수신:
          - 메시지 DB 저장
          - 그룹에 새 메시지 broadcast
        """
        data = json.loads(text_data)
        
        if data.get('command') == 'fetch_messages':
            # 기존 메시지 목록을 DB에서 가져와서 한 번에 전송
            messages = await self.get_existing_messages()
            await self.send(text_data=json.dumps({"messages": messages}))
        elif data.get('content'):
            message_content = data['content']
            msg = await self.save_message(message_content)
            # 그룹 내 모든 사용자에게 새 메시지 브로드캐스트
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': msg.id,
                    'content': msg.content,
                    'sender_id': self.user.id,
                    'sender_nickname': self.user.nickname,
                    'profile_image': self.user.profile_image.url if self.user.profile_image else None,
                    'timestamp': msg.timestamp.isoformat(),
                }
            )

    async def chat_message(self, event):
        """
        그룹에서 broadcast된 메시지 수신:
          - 클라이언트에 WebSocket 메시지 전송
          - 본인이 보낸 메시지가 아닌 경우 읽음 처리
        """
        await self.send(text_data=json.dumps(event))
        if event['sender_id'] != self.user.id:
            await self.mark_as_read(event['message_id'])

    @database_sync_to_async
    def get_existing_messages(self):
        room = ChatRoom.objects.get(id=self.room_id)
        messages = list(room.messages.order_by('timestamp').select_related('sender'))
        msg_list = []
        for message in messages:
            # DB에서 현재 사용자가 메시지 읽음 여부를 판별
            is_read = message.read_by.filter(id=self.user.id).exists()
            msg_list.append({
                'message_id': message.id,
                'content': message.content,
                'sender_id': message.sender.id,
                'sender_nickname': message.sender.nickname,
                'profile_image': message.sender.profile_image.url if message.sender.profile_image else None,
                'timestamp': message.timestamp.isoformat(),
                'is_read': is_read,
            })
        return msg_list

    @database_sync_to_async
    def validate_participation(self):
        return ChatRoom.objects.filter(
            Q(user1=self.user) | Q(user2=self.user),
            id=self.room_id
        ).exists()

    @database_sync_to_async
    def save_message(self, content):
        """메시지를 DB에 저장하고 반환"""
        room = ChatRoom.objects.get(id=self.room_id)
        message = Message.objects.create(
            room=room,
            sender=self.user,
            content=content
        )
        message.read_by.add(self.user)  # 보낸 사람은 자동으로 읽음 처리
        room.update_last_message_time()
        return message

    @database_sync_to_async
    def mark_as_read(self, message_id):
        """메시지를 읽음 처리"""
        message = Message.objects.get(id=message_id)
        message.read_by.add(self.user)

    @database_sync_to_async
    def get_user_from_token(self, token):
        """
        JWT 토큰을 검증하고 사용자 객체를 반환.
        토큰이 없거나 검증에 실패하면 AnonymousUser 반환.
        """
        if not token:
            return self.scope.get("user", AnonymousUser())
        try:
            UntypedToken(token)
            user = User.objects.get(id=UntypedToken(token).payload['user_id'])
            return user
        except (InvalidToken, TokenError, User.DoesNotExist):
            return AnonymousUser()
