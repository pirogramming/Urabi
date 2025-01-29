from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'user_name', 'user_age', 'user_gender', 'user_phone', 'nickname', 'profile_image', 'trust_score', 'created_at']
        read_only_fields = ['id', 'trust_score', 'created_at']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'user_name', 'user_age', 'user_gender', 'user_phone', 'nickname', 'profile_image']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user