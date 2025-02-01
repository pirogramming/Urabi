from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.conf import settings
from .models import User
import requests
from django.core.files.storage import FileSystemStorage
import json
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import render
from .models import User
from .serializers import SignupSerializer, UserSerializer, LoginSerializer


def social_login(request):
    return render(request, 'users/social_login.html')

def kakao_login(request):
    client_id = settings.KAKAO_API_KEY
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_login_callback(request):
    code = request.GET.get("code")
    client_id = settings.KAKAO_API_KEY
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"  

    token_request = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    token_json = token_request.json()
    
    if "error" in token_json:
        return redirect('users:login')

    access_token = token_json.get("access_token")
    
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    
    kakao_account = profile_json.get("kakao_account", {})
    email = kakao_account.get("email")
    
    if not email:
        kakao_id = profile_json.get("id")
        email = f"kakao_{kakao_id}@example.com"  # 카카오 ID를 활용한 임시 이메일 생성
        properties = profile_json.get("properties", {})
        nickname = properties.get("nickname")
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            social_id=f"kakao_{profile_json.get('id')}",
            first_name=nickname,
            nickname=nickname,
        )

    login(request, user)
    return redirect('users:main')  

def naver_login(request):
    client_id = settings.NAVER_CLIENT_ID
    redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback/"
    state = "RANDOM_STATE"
    
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&state={state}"
    )

def naver_login_callback(request):
    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET
    redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback/"  
    code = request.GET.get("code")
    state = request.GET.get("state")
    
    token_request = requests.post(
        "https://nid.naver.com/oauth2.0/token",
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
            "state": state,
        },
    )
    token_json = token_request.json()
    
    if "error" in token_json:
        return redirect("/")
        
    access_token = token_json.get("access_token")
    profile_request = requests.get(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    
    if profile_json.get("resultcode") != "00":
        return redirect("/")
        
    response = profile_json.get("response")
    email = response.get("email")
    name = response.get("name")
    profile_image = response.get("profile_image")
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            social_id=f"naver_{response.get('id')}",
            first_name=name,
        )
        if profile_image:
            user.profile_image = profile_image
            user.save()
    
    login(request, user)
    return redirect('users:main')

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        if request.content_type == 'application/json':
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
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            
            if user:
                login(request, user)
                return redirect('users:main')
            return render(request, 'login/login.html', {'error': '로그인 실패'})

    def get(self, request):
        return render(request, 'login/login.html')

def signup_view(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            name = request.POST.get('name')
            nickname = request.POST.get('nickname')
            birth_year = request.POST.get('birth-year')
            birth_month = request.POST.get('birth-month')
            birth_day = request.POST.get('birth-day')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            profile_image = request.FILES.get('profile-picture')
            
            # 이메일 중복 체크
            if User.objects.filter(email=email).exists():
                return render(request, 'register/register.html', {'error': '이미 존재하는 이메일입니다.'})
            
            # 성별 값 변환
            gender = 'M' if gender == 'male' else 'F'
            
            # 나이 계산 (예시)
            from datetime import datetime
            current_year = datetime.now().year
            age = current_year - int(birth_year)
            
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=name,
                nickname=nickname,
                user_age=age,
                user_gender=gender,
                user_phone=phone
            )
            
            if profile_image:
                fs = FileSystemStorage()
                filename = fs.save(f'profile_images/{profile_image.name}', profile_image)
                user.profile_image = filename
                user.save()
            
            # 회원가입 후 자동 로그인
            login(request, user)
            return redirect('users:main')
            
        except Exception as e:
            print(f"회원가입 에러: {str(e)}")  # 디버깅용 로그
            return render(request, 'register/register.html', {'error': str(e)})
    
    return render(request, 'register/register.html')

def user_logout(request):
    logout(request)
    return redirect('users:main')

def login_view(request):
    return render(request, 'main/main.html', {'user': request.user})

def main_view(request):
    print(f"🔍 현재 로그인된 사용자: {request.user}")  
    print(f"🔍 인증 여부: {request.user.is_authenticated}")  
    return render(request, 'main/main.html')

