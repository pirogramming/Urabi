from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import get_csrf_token
from .views import get_token_for_logged_in_user

app_name = 'users'

urlpatterns = [
    path('users/', views.login_view, name='main'),  
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/kakao/', views.kakao_login, name='kakao-login'),
    path('login/kakao/callback/', views.kakao_login_callback, name='kakao-callback'),
    path('login/naver/', views.naver_login, name='naver-login'),
    path('login/naver/callback/', views.naver_login_callback, name='naver-callback'),
    path('logout/', views.user_logout, name='logout'),

     path('register/phone_verification/', views.phone_verification, name='phone_verification'),
    path('register/verify_phone_status/', views.verify_phone_status, name='verify_phone_status'),

    path('mypage/', views.my_page, name='my_page'),
    path("csrf/", views.get_csrf_token, name="get_csrf_token"),
    path('api/get_token/', views.get_token_for_logged_in_user, name='get_token'),
    path('api/some-protected-route/', views.some_protected_route, name='some_protected_route'),

    path('mypage/edit/', views.edit_profile, name='edit_profile'),
    path('mypage/trip/<int:pk>', views.my_trip, name='my_trip'),
    path('mypage/trip/update/<int:pk>', views.update_trip, name='update_trip'),
    path('mypage/trip/delete/<int:pk>/', views.delete_trip, name='delete_trip'),
    path('mypage/detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('mypage/plan/<int:pk>/', views.plan_detail, name='plan_detail'),
    path('mypage/list/', views.user_list, name='user_list'),
    path('mypage/zzim/', views.zzim_list, name='zzim_list'),
    path('mypage/schedule/create/', views.schedule_create, name='schedule_create'),
    path('mypage/schedule/detail/<int:pk>/', views.schedule_detail, name='schedule_detail'),
    path('delete_schedule/', views.delete_schedule, name='delete_schedule'),
    path('phone-verification/', views.phone_verification, name='phone_verification'),
    path('verify-phone-status/', views.verify_phone_status, name='verify_phone_status'),
    path('check-phone/', views.check_phone_duplicate, name='check_phone_duplicate'),
    path('update_schedule_photo/', views.update_schedule_photo, name='update_schedule_photo'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)