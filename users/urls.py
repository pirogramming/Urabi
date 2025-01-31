from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    #path('', views.login_view, name='main'),  
    path('main/', views.main_view, name='main'), 
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/kakao/', views.kakao_login, name='kakao-login'),
    path('login/kakao/callback/', views.kakao_login_callback, name='kakao-callback'),
    path('login/naver/', views.naver_login, name='naver-login'),
    path('login/naver/callback/', views.naver_login_callback, name='naver-callback'),
    path('logout/', views.user_logout, name='logout'),


    path('accompany/', include('accompany.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)