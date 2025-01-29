from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.main, name='main'),
    #path('signup/', views.signup, name='signup'),  
    path('login/', views.login_view, name='login'),  
    path('login/kakao/', views.kakao_login, name='kakao-login'),
    path('login/kakao/callback/', views.kakao_login_callback, name='kakao-callback'),
    path('login/naver/', views.naver_login, name='naver-login'),
    path('login/naver/callback/', views.naver_login_callback, name='naver-callback'),
]