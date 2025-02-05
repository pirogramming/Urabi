from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path("main/", views.chat_main, name="chat_main"),
    path("create/", views.create_chat_room, name="create_chat_room"),

    path('rooms/', views.ChatRoomList.as_view(), name='chat_room_list'),  # 채팅방 목록 조회
    path("room/<int:room_id>/", views.chat_room, name="chat_room"),  # 특정 채팅방 입장
    path('rooms/<int:room_id>/messages/', views.get_chat_messages, name='get_chat_messages'), # 특정 채팅방의 메시지 목록 조회
    path('messages/<int:message_id>/', views.delete_message, name='delete_message'), # 특정 메시지 삭제
    path('rooms/<int:room_id>/details/', views.get_chat_room_details, name='get_chat_room_details'), # 채팅방 상세 정보 조회
    path('messages/<int:message_id>/read/', views.mark_as_read, name='mark_message_as_read'), # 메시지 읽음 표시
    path('some-protected-route/', views.some_protected_route, name='some_protected_route'),
    
]