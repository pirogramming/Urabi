from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Max
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, ChatRoomInfoSerializer, MessageSerializer, ChatRoomDetailSerializer
from users.models import User
from accompany.models import TravelGroup
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()
@login_required
def chat_main(request):
    user = request.user
    error_message = ""
    searched_users = []  # 검색 결과 유저 리스트

    if request.method == "POST":
        search_email = request.POST.get("other_email", "").strip()

        if not search_email:
            error_message = "이메일을 입력하세요."
        elif search_email == user.email:
            error_message = "자기 자신과 채팅할 수 없습니다."
        else:
            searched_users = User.objects.filter(email__icontains=search_email).exclude(id=user.id)
            if not searched_users.exists():
                error_message = "해당 이메일을 가진 사용자를 찾을 수 없습니다."

    # 채팅방 목록
    rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user)).order_by('-last_message_time')
    for room in rooms:
        if room.user1 == user:
            room.other_user = room.user2
        else:
            room.other_user = room.user1

        last_msg = room.messages.order_by('-timestamp').first()
        room.last_message = last_msg.content if last_msg else None
        
        unread_count = room.messages.filter(~Q(sender=user), ~Q(read_by=user)).count()
        room.unread_count = unread_count
        
    context = {
        'room_list': rooms,
        'searched_users': searched_users,
        'error_message': error_message,
    }
    return render(request, 'chat/chat_main.html', context)


@login_required
def create_chat_room(request, user_id):
    """유저 클릭 시 해당 유저와 채팅방으로 이동(없으면 생성)"""
    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)

    if current_user == other_user:
        return HttpResponse("자기 자신과는 채팅할 수 없습니다.", status=400)

    # 채팅방 중복 여부 확인
    room = ChatRoom.objects.filter(
        (Q(user1=current_user) & Q(user2=other_user)) |
        (Q(user1=other_user) & Q(user2=current_user))
    ).first()

    if not room:
        room = ChatRoom.objects.create(user1=current_user, user2=other_user)

    return redirect('chat:chat_room', room_id=room.id)

# 채팅방 목록 페이지네이션 
class ChatRoomPagination(PageNumberPagination):
    page_size = 20 # 한 페이지당 표시할 채팅방 수
    page_size_query_param = 'page_size'

# 채팅방 목록 조회 및 생성 API 뷰
class ChatRoomList(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ChatRoomPagination

    def get_queryset(self):
        # 현재 사용자가 참여한 채팅방 목록 조회
        user = self.request.user
        return ChatRoom.objects.filter(Q(user1=user) | Q(user2=user)).order_by('-last_message_time')

    def create(self, request, *args, **kwargs):
        # 새로운 채팅방 생성 로직
        user1_id = request.user.id
        user2_id = request.data.get('user2')
        travel_id = request.data.get('travel')
        
        # 상대방 사용자 존재 여부 확인
        if not User.objects.filter(id=user2_id).exists():
            return Response({'error': '상대방 사용자가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        travel = get_object_or_404(TravelGroup, travel_id=travel_id)
        if not travel.participants.filter(id__in=[user1_id, user2_id]).count() == 2:
            return Response({'error': '두 사용자 모두 해당 여행에 참여하고 있어야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 존재하는 채팅방 확인
        existing_room = ChatRoom.objects.filter(
            (Q(user1_id=user1_id, user2_id=user2_id) | Q(user1_id=user2_id, user2_id=user1_id)),
            travel_id=travel_id
        ).first()

        if existing_room:
            serializer = self.get_serializer(existing_room)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # 새 채팅방 생성
        serializer = self.get_serializer(data={
            'user1': user1_id,
            'user2': user2_id,
            'travel': travel_id
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 채팅방 목록 조회 API
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def chat_rooms(request):
    user = request.user
    # 사용자가 참여한 채팅방 목록 조회 및 정보 집계
    rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user)).annotate(
        unread_count=Count('messages', filter=Q(messages__read_by=False, messages__sender__ne=user)),
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time')

    paginator = ChatRoomPagination()
    paginated_rooms = paginator.paginate_queryset(rooms, request)

    chat_rooms_data = []
    for room in paginated_rooms:
        other_user = room.user2 if room.user1 == user else room.user1
        last_message = room.messages.order_by('-timestamp').first()

        room_data = {
            'id': room.id,
            'other_user_id': other_user.id,
            'other_user_nickname': other_user.nickname,
            'other_user_profile_image': request.build_absolute_uri(other_user.profile_image.url) if other_user.profile_image else None,
            'last_message_content': last_message.content if last_message else None,
            'last_message_timestamp': last_message.timestamp if last_message else None,
            'unread_count': room.unread_count,
            'travel_title': room.travel.title,
        }
        chat_rooms_data.append(room_data)

    return paginator.get_paginated_response(ChatRoomInfoSerializer(chat_rooms_data, many=True).data)



# 채팅방 입장 API
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def enter_chat_room(request, room_id):
    """
    채팅방 입장 API
    - 현재 요청한 사용자가 채팅방에 참여 중인지 확인하고,
    - 읽지 않은 메시지를 읽음 처리하고,
    - WebSocket 연결 URL(토큰 포함) 등 채팅방 상세 정보를 반환합니다.
    """
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    user = request.user

    if user not in [chat_room.user1, chat_room.user2]:
        return Response({'error': '이 채팅방에 접근할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    other_user = chat_room.user2 if user == chat_room.user1 else chat_room.user1

    # 읽지 않은 메시지 읽음 처리
    messages = Message.objects.filter(room=chat_room, sender=other_user)
    for msg in messages:
        msg.read_by.add(request.user)
    
    auth_header = request.headers.get("Authorization", "")
    token = ""
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]

    # 채팅방 정보 응답
    response_data = {
        'room_id': chat_room.id,
        'room_name': f"{chat_room.user1.nickname} - {chat_room.user2.nickname}",
        'other_user_nickname': other_user.nickname,
        'other_user_profile_image': request.build_absolute_uri(other_user.profile_image.url) if other_user.profile_image else None,
        'websocket_url': f"wss://{request.get_host()}/ws/chat/{chat_room.id}/?token={token}"
    }

    return Response(response_data, status=status.HTTP_200_OK)

# 채팅 메시지 조회 API
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_chat_messages(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    user = request.user

    # 메시지 조회 권한 확인
    if user not in [chat_room.user1, chat_room.user2]:
        return Response({'error': '이 채팅방의 메시지를 볼 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    messages = Message.objects.filter(room=chat_room).order_by('-timestamp')
    
    paginator = ChatRoomPagination()
    paginated_messages = paginator.paginate_queryset(messages, request)
    
    serializer = MessageSerializer(paginated_messages, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

# 메시지 삭제 API
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # 메시지 삭제 권한 확인
    if message.sender != request.user:
        return Response({'error': '이 메시지를 삭제할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    # 메시지 삭제 가능 시간 확인 (5분 이내)
    if (timezone.now() - message.timestamp).total_seconds() > 300:  
        return Response({'error': '메시지 전송 후 5분이 지나 삭제할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    message.delete()
    return Response({'message': '메시지가 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

# 채팅방 상세 정보 조회 API
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_chat_room_details(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    user = request.user

    if user not in [chat_room.user1, chat_room.user2]:
        return Response({'error': '이 채팅방의 정보를 볼 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ChatRoomDetailSerializer(chat_room, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
  
# 메시지 읽음 표시 API
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    user = request.user

    if user not in [message.room.user1, message.room.user2]:
        return Response({'error': '이 메시지를 읽을 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    # 메시지 읽음 처리
    if user != message.sender and user not in message.read_by.all():
        message.read_by.add(user)
        return Response({'message': '메시지를 읽음으로 표시했습니다.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': '이미 읽은 메시지입니다.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def some_protected_route(request):
    return Response({'message': 'This is a protected route!'}, status=status.HTTP_200_OK)

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in [room.user1, room.user2]:
        return HttpResponse("No Permission", status=403)

    other_user = room.user2 if room.user1 == request.user else room.user1
    unread_msgs = room.messages.filter(sender=other_user).exclude(read_by=request.user)
    
    channel_layer = get_channel_layer()
    for m in unread_msgs:
        m.read_by.add(request.user)
        async_to_sync(channel_layer.group_send)(
            f"chat_{room.id}",
            {
                "type": "chat.read_event",  
                "message_id": m.id,
                "reader_id": request.user.id,
            }
        )

    return render(request, 'chat/room_chat.html', {
        'room': room,
        'access_token': "",
    })