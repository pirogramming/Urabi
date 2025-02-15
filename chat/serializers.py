from rest_framework import serializers
from .models import ChatRoom, Message
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'profile_image']
    
    def get_profile_image(self, obj):
        request = self.context.get("request")
        if request and obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return ""

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source="sender.email", read_only=True)
    sender_nickname = serializers.CharField(source="sender.nickname", read_only=True)
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id',
            'room',
            'sender_email',
            'sender_nickname',
            'profile_image_url',
            'content',
            'timestamp',
            'read_by',
        ]
    
    def get_profile_image_url(self, obj):
        request = self.context.get("request")
        if request and obj.sender.profile_image:
            return request.build_absolute_uri(obj.sender.profile_image.url)
        return ""

class ChatRoomSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'user1', 'user2', 'travel', 'created_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Request context is required.")
        validated_data['user1'] = request.user
        if 'user2' in self.initial_data:
            validated_data['user2_id'] = self.initial_data['user2']
        if 'travel' in self.initial_data:
            validated_data['travel_id'] = self.initial_data['travel']
        return super().create(validated_data)

class ChatRoomInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    other_user_id = serializers.IntegerField()
    other_user_nickname = serializers.CharField()
    other_user_profile_image = serializers.URLField(allow_null=True)
    last_message_content = serializers.CharField(allow_null=True)
    last_message_timestamp = serializers.DateTimeField(allow_null=True)
    unread_count = serializers.IntegerField()
    travel_title = serializers.CharField()

class ChatRoomDetailSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = [
            'id',
            'user1',
            'user2',
            'travel',
            'created_at',
            'last_message_time',  
            'messages',
        ]
