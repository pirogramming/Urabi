from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import render
from .models import User
from .serializers import SignupSerializer, UserSerializer, LoginSerializer

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user_id": user.id,
            "email": user.email,
            "nickname": user.nickname,
            "profile_image": user.profile_image.url if user.profile_image else None,
            "trust_score": user.trust_score,
            "created_at": user.created_at.isoformat(),
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "token": str(refresh.access_token),
                "user": {
                    "user_id": user.id,
                    "nickname": user.nickname,
                    "profile_image": user.profile_image.url if user.profile_image else None,
                }
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

def signup_page(request):
    return render(request, 'login/signup.html')

def login_page(request):
    return render(request, 'login/login.html')