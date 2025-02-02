from rest_framework import serializers
from .models import ChatRoom, Message
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    사용자 정보 직렬화 클래스
    - 목적: 사용자 모델의 특정 필드를 API 응답에 포함시키기 위해 사용
    - 포함 필드:
      - id: 사용자 고유 식별자
      - nickname: 사용자 닉네임
      - profile_image: 프로필 이미지 URL
    """
    class Meta:
        model = User
        fields = ['id', 'nickname', 'profile_image']

class MessageSerializer(serializers.ModelSerializer):
    """
    채팅 메시지 직렬화 클래스
    - 메시지 모델의 데이터를 JSON 형식으로 변환
      - sender 필드는 UserSerializer를 사용해 중첩 직렬화
      - read_by: 메시지를 읽은 사용자 목록
    """
    
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'timestamp', 'read_by']

class ChatRoomSerializer(serializers.ModelSerializer):
    """
    채팅방 상세 정보 직렬화 클래스
    - 채팅방의 모든 세부 정보 표현
      - user1/user2: 중첩된 사용자 정보 표현
      - travel: 연결된 여행 그룹 ID 자동 포함
    """
    user1 = UserSerializer(read_only=True)  # 사용자1 상세 정보
    user2 = UserSerializer(read_only=True)  # 사용자2 상세 정보
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'user1', 'user2', 'travel', 'created_at']

class ChatRoomInfoSerializer(serializers.Serializer):
    """
    채팅방 목록 표시용 최적화 직렬화 클래스
    - 채팅방 목록에서 필요한 정보만 전달
    - 데이터:
      - id: 채팅방 ID
      - other_user_*: 상대방 사용자 정보
      - last_message_*: 최근 메시지 정보
      - unread_count: 안 읽은 메시지 수
      - travel_title: 연결된 여행 제목
    """
    id = serializers.IntegerField()
    other_user_id = serializers.IntegerField()
    other_user_nickname = serializers.CharField()
    other_user_profile_image = serializers.URLField(allow_null=True) # 이미지 없을 경우 null
    last_message_content = serializers.CharField(allow_null=True)    # 메시지 없을 경우 null
    last_message_timestamp = serializers.DateTimeField(allow_null=True)
    unread_count = serializers.IntegerField()
    travel_title = serializers.CharField()   # TravelGroup의 title 필드 매핑