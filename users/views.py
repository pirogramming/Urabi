from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.conf import settings
from .models import User
import requests

def social_login(request):
    return render(request, 'users/social_login.html')

def kakao_login(request):
    client_id = settings.KAKAO_API_KEY
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_login_callback(request):
    code = request.GET.get("code")
    client_id = settings.KAKAO_API_KEY
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"

    # 토큰 요청
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
        return redirect("/")

    access_token = token_json.get("access_token")
    
    # 프로필 정보 요청
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    
    # 카카오 계정 정보 확인
    kakao_account = profile_json.get("kakao_account", {})
    email = kakao_account.get("email")
    
    if not email:
        return redirect("/")
    
    properties = profile_json.get("properties", {})
    nickname = properties.get("nickname", "Unknown")
    profile_image = properties.get("profile_image")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            social_id=f"kakao_{profile_json.get('id')}",
            first_name=nickname,
        )
        if profile_image:
            user.profile_image = profile_image
            user.save()

    login(request, user)
    return redirect('users:main')

def naver_login(request):
    client_id = settings.NAVER_CLIENT_ID
    redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback"
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
    code = request.GET.get("code")
    state = request.GET.get("state")
    
    token_request = requests.post(
        "https://nid.naver.com/oauth2.0/token",
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
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

def main(request):
    return render(request, 'login/login.html', {'user': request.user})

def user_logout(request):
    logout(request)
    return redirect('users:main')
  
def login_view(request):
    return render(request, 'login/login.html')
