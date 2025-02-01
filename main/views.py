from django.shortcuts import render



# Create your views here.
def main_view(request):
    print(f"🔍 현재 로그인된 사용자: {request.user}")  
    print(f"🔍 인증 여부: {request.user.is_authenticated}")  
    return render(request, 'main/main.html')