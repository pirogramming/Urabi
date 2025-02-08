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
                "sender_nickname": self.user.nickname,
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
            await self.notify_room_users(msg)


    async def chat_message(self, event):
    # "chat_message" 타입 이벤트를 수신
        logger.debug(f"chat_message 호출됨")
        await self.send(text_data=json.dumps(event))
        if event["sender_id"] != self.user.id:
            await self.mark_as_read(event["message_id"])
            await self.notify_message_read(event["message_id"], self.user.id)

            read_event = {
                "type": "chat_read_event",
                "message_id": event["message_id"],
                "reader_id": self.user.id
            }

            await self.channel_layer.group_send(
                self.room_group_name,
                read_event

            )

    # 메시지 읽음 이벤트 수신
    async def chat_read_event(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat.read_event",
            "message_id": event["message_id"],
            "reader_id": event["reader_id"]
        }))

        
   
    async def notify_room_users(self, new_msg):
        room = await self.get_room()
        user1_id, user2_id = room.user1_id, room.user2_id

        unread1 = await self.get_unread_count(room, user1_id)
        unread2 = await self.get_unread_count(room, user2_id)
        last_msg_content = new_msg.content
        last_msg_ts = new_msg.timestamp.isoformat()

        # 동기 메서드 접근을 비동기 호출로 감싸기
        other_user_nickname_user1 = await database_sync_to_async(lambda: room.user2.nickname)()
        other_user_profile_image_user1 = await database_sync_to_async(
            lambda: room.user2.profile_image.url if room.user2.profile_image else "/media/profile_images/default-profile.png"
        )()

        other_user_nickname_user2 = await database_sync_to_async(lambda: room.user1.nickname)()
        other_user_profile_image_user2 = await database_sync_to_async(
            lambda: room.user1.profile_image.url if room.user1.profile_image else "/media/profile_images/default-profile.png"
        )()

        # user1에게 전송: user1의 상대는 user2
        await self.channel_layer.group_send(
            f"user_{user1_id}",
            {
                "type": "user_notification",
                "room_id": room.id,
                "unread_count": unread1,
                "last_message_content": last_msg_content,
                "last_message_timestamp": last_msg_ts,
                "other_user_nickname": other_user_nickname_user1,
                "other_user_profile_image": other_user_profile_image_user1
            }
        )

        # user2에게 전송: user2의 상대는 user1
        await self.channel_layer.group_send(
            f"user_{user2_id}",
            {
                "type": "user_notification",
                "room_id": room.id,
                "unread_count": unread2,
                "last_message_content": last_msg_content,
                "last_message_timestamp": last_msg_ts,
                "other_user_nickname": other_user_nickname_user2,
                "other_user_profile_image": other_user_profile_image_user2
            }
        )

    async def notify_message_read(self, message_id, reader_id):
        """
        sender에게 '메시지가 읽혔음' 알림
        => sender can show "V" or "read"
        """
        msg = await self.get_message(message_id)
        sender_id = msg.sender_id
        if sender_id != reader_id:  # 자기 자신이 보낸 메시지면 X
            await self.channel_layer.group_send(
                f"user_{sender_id}",
                {
                    "type": "user_notification",
                    "event": "message_read",
                    "message_id": message_id,
                    "reader_id": reader_id
                }
            )
    
    @database_sync_to_async
    def get_room(self):
        return ChatRoom.objects.get(id=self.room_id)

    @database_sync_to_async
    def get_message(self, message_id):
        return Message.objects.get(id=message_id)

    @database_sync_to_async
    def get_unread_count(self, room, user_id):
        return room.messages.filter(~Q(sender_id=user_id), ~Q(read_by__id=user_id)).count()

    @database_sync_to_async
    def get_existing_messages(self):
        room = ChatRoom.objects.get(id=self.room_id)
        messages = list(room.messages.order_by("timestamp").select_related("sender"))
        my_id = self.user.id
        
        msg_list = []
        for message in messages:
            is_read_by_me = message.read_by.filter(id=my_id).exists()

            if message.sender_id == my_id:
                other_id = room.user2_id if room.user1_id == my_id else room.user1_id
                is_read_by_other = message.read_by.filter(id=other_id).exists()
            else:
                is_read_by_other = False  # 또는 None

            msg_list.append({
                "message_id": message.id,
                "content": message.content,
                "sender_id": message.sender.id,
                "sender_nickname": message.sender.nickname,
                "timestamp": message.timestamp.isoformat(),
                "is_read": is_read_by_me,  
                "is_read_by_other": is_read_by_other,
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
        msg = Message.objects.get(id=message_id)
        msg.read_by.add(self.user)

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
    
    async def notify_users(self, room, new_msg):
        user1_id = room.user1_id
        user2_id = room.user2_id
        
        # unread counts
        unread_count_user1 = await self.get_unread_count(room, user1_id)
        unread_count_user2 = await self.get_unread_count(room, user2_id)

        last_message_content = new_msg.content
        last_message_ts = new_msg.timestamp.isoformat()

        # broadcast
        for uid, uc in [(user1_id, unread_count_user1), (user2_id, unread_count_user2)]:
            await self.channel_layer.group_send(
                f"user_{uid}",
                {
                    "type": "user_notification",
                    "room_id": room.id,
                    "unread_count": uc,
                    "last_message_content": last_message_content,
                    "last_message_timestamp": last_message_ts
                }
            )

class UserConsumer(AsyncWebsocketConsumer):
    """
    각 유저가 chat_main 페이지에서 접속: /ws/user/<user_id>/
    새로운 메시지 or 메시지 읽음 이벤트를 받아 실시간 목록 갱신
    """
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f"user_{self.user_id}"

        # 로그인 사용자인지 확인
        if self.scope["user"].id != int(self.user_id):
            await self.close()
            return

        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()
        logger.debug(f"[UserConsumer] user_{self.user_id} 연결됨")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)
        logger.debug(f"[UserConsumer] user_{self.user_id} 해제됨")

    async def receive(self, text_data):
        data = json.loads(text_data)
        # 필요 시 명령 처리

    async def user_notification(self, event):
        await self.send(text_data=json.dumps(event))