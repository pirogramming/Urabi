# chat/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ChatRoom(models.Model):
    """
    두 사용자가 채팅할 수 있는 채팅방.
    """
    user1 = models.ForeignKey(User, related_name='user1_chatrooms', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2_chatrooms', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_time = models.DateTimeField(null=True, blank=True)
    deleted_at_user1 = models.DateTimeField(null=True, blank=True)
    deleted_at_user2 = models.DateTimeField(null=True, blank=True)



    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-last_message_time', '-created_at']

    def __str__(self):
        return f"{self.user1.nickname} "

    @property
    def chat_group_name(self):
        """채팅 그룹 이름, WebSocket 그룹에 사용"""
        return f"chat_{self.id}"

    def update_last_message_time(self):
        self.last_message_time = timezone.now()
        self.save()


class Message(models.Model):
    """
    채팅 메시지 모델.
    """
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # 읽은 사용자 목록 (ManyToManyField)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)
    deleted_by = models.ManyToManyField(User, related_name='deleted_messages', blank=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.room.update_last_message_time()
