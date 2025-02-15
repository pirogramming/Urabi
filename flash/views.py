from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Flash, FlashZzim, FlashParticipants, FlashRequest
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models import F
from .filters import FlashFilter
import json


def flash_list(request):
    flash_meetings = Flash.objects.all().order_by("-created_at")
    filterset = FlashFilter(request.GET, queryset=flash_meetings)

    # 현재 로그인한 유저의 찜 목록 가져오기
    zzim_items = set()
    if request.user.is_authenticated:
        zzim_items = set(FlashZzim.objects.filter(user=request.user).values_list("flash_id", flat=True))


    for flash in flash_meetings:
        flash.tag_list = flash.tags.split(",") if flash.tags else []
        flash.image_url = f"https://maps.googleapis.com/maps/api/streetview?size=500x500&location={flash.latitude},{flash.longitude}&key={settings.GOOGLE_MAPS_API_KEY}"
        flash.is_zzimmed = flash.pk in zzim_items  # 찜 여부 추가
        flash.current_participants = FlashParticipants.objects.filter(flash=flash).count()

    return render(request, "flash/flash_list.html", {"flash_meetings": flash_meetings, 'filterset': filterset, "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY})


@login_required
def flash_register(request):
    if request.method == "POST":
        title = request.POST.get("title")
        city = request.POST.get("location")  # 사용자가 입력한 장소
        latitude = request.POST.get('latitude', 0.0) or 0.0  # 숨겨진 input으로 위도 전달
        longitude = request.POST.get('longitude', 0.0) or 0.0  # 숨겨진 input으로 경도 전달
        date_time = request.POST.get("date")
        max_people = request.POST.get("capacity")
        explanation = request.POST.get("description")
        tags = request.POST.get("tags", "")

        # Flash 모델에 저장
        flash = Flash.objects.create(
            title=title,
            city=city,
            latitude=latitude,
            longitude=longitude,
            date_time=date_time,
            max_people=max_people,
            explanation=explanation,
            tags=tags,
            created_by=request.user,  # 현재 로그인한 사용자
            created_at=now(),
            updated_at=now(),
        )
        return redirect("flash:flash_list")  # 리스트 페이지로 이동
    
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY  # API 키 전달
    }

    return render(request, "flash/flash_register.html", context)

@login_required
def flash_update(request, pk):
    flash = get_object_or_404(Flash, pk=pk)

    # 작성자만 수정 가능
    if request.user != flash.created_by:
        return redirect("flash:flash_list")

    if request.method == "POST":
        flash.title = request.POST.get("title")
        flash.city = request.POST.get("location")
        flash.latitude = request.POST.get("latitude", 0.0) or 0.0
        flash.longitude = request.POST.get("longitude", 0.0) or 0.0
        flash.date_time = request.POST.get("date")
        flash.max_people = request.POST.get("capacity")
        flash.explanation = request.POST.get("description")
        flash.tags = request.POST.get("tags", "")
        flash.updated_at = now()
        flash.save()
        return redirect("flash:flash_detail", pk=flash.pk)

    return render(request, "flash/flash_register.html", {"flash": flash, "edit_mode": True})


@login_required
def flash_delete(request, pk):
    flash = get_object_or_404(Flash, pk=pk)

    if request.user == flash.created_by:  # 작성자인지 확인
        flash.delete()
        return JsonResponse({"message": "삭제되었습니다."}, status=200)
    
    return JsonResponse({"error": "삭제 권한이 없습니다."}, status=403)


def flash_detail(request, pk):
    flash = get_object_or_404(Flash, pk=pk)  # 해당 ID의 번개 모임 조회
    
    # tags를 리스트로 변환 (flash.tags가 존재하는 경우만 split)
    tag_list = flash.tags.split(",") if flash.tags else []

    # 찜 여부 확인
    is_zzimmed = False
    if request.user.is_authenticated:
        is_zzimmed = FlashZzim.objects.filter(user=request.user, flash=flash).exists()

    # 현재 참가 중인 유저 리스트
    participants = FlashParticipants.objects.filter(flash=flash).select_related("user")
    participant_data = [
        {"id": p.user.id, "email": p.user.email} for p in participants
    ]

    participant_ids = [p["id"] for p in participant_data]  # ID 리스트 추출
    

    # 현재 참가 요청을 보낸 유저 리스트
    pending_requests = list(FlashRequest.objects.filter(flash=flash).values_list("user_id", flat=True))

    # 현재 번개와 가장 가까운 2개의 번개 찾기 (pk 기준으로 가장 가까운 번개)
    other_flash_meetings = Flash.objects.exclude(pk=pk).order_by(F('pk') - pk)[:2]

    flash_img = None
    if f'flash_img_{pk}' in request.session:
        flash_img = request.session[f'flash_img_{pk}']

    # 다른 번개들도 이미지 URL 설정
    for other_flash in other_flash_meetings:
        session_img_key = f'flash_img_{other_flash.pk}'
        if session_img_key in request.session:
            other_flash.image_url = request.session[session_img_key]  # 세션에서 이미지 가져오기
        elif other_flash.latitude and other_flash.longitude:
            other_flash.image_url = f"https://maps.googleapis.com/maps/api/streetview?size=500x500&location={other_flash.latitude},{other_flash.longitude}&key={settings.GOOGLE_MAPS_API_KEY}"
        else:
            other_flash.image_url = "/static/img/default_map_image.jpg"

    return render(request, "flash/flash_detail.html", {
        "flash": flash, 
        "tag_list": tag_list,
        "is_zzimmed": is_zzimmed,
        "flash_img": flash_img,
        "other_flash_meetings": other_flash_meetings,
        "participants": participants,
        "pending_requests": pending_requests,
        "participant_ids" : participant_ids,
        "participant_data": participant_data,
        }
    )

def save_flash_img(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            flash_id = data.get("flash_id")
            img_src = data.get("img_src")

            print("🔄 flash_id:", flash_id)  # 디버깅
            print("🖼 img_src:", img_src)  # 디버깅

            if flash_id and img_src:
                request.session[f'flash_img_{flash_id}'] = img_src
                request.session.save()
                return JsonResponse({"message": "이미지 저장 완료"}, status=200)
            else:
                return JsonResponse({"error": "flash_id 또는 img_src 없음"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "잘못된 요청"}, status=400)



@login_required
def flash_zzim(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "로그인이 필요합니다."}, status=403)
    
    flash = get_object_or_404(Flash, pk=pk)
    user = request.user

    zzim, created = FlashZzim.objects.get_or_create(user=user, flash=flash)

    if not created:
        zzim.delete()  # 이미 찜한 경우 삭제
        return JsonResponse({"zzimmed": False})
    
    return JsonResponse({"zzimmed": True})

@csrf_exempt
@login_required
def add_flash_participant(request):
    if request.method == "POST":
        User = get_user_model()
        try:
            data = json.loads(request.body)
            flash_id = data.get("flash_id")
            user_id = data.get("user_id")

            flash = get_object_or_404(Flash, meeting_id=flash_id)
            user = get_object_or_404(User, id=user_id)

            print(f"🔍 Flash: {flash.meeting_id}, User: {user.id}")

            # 참가 요청 삭제 후 참가자로 추가
            FlashRequest.objects.filter(flash=flash, user=user).delete()
            FlashParticipants.objects.create(flash=flash, user=user)
            flash.now_member += 1
            flash.save()

            return JsonResponse({"message": "참가 완료!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)


@login_required
@csrf_exempt
def remove_flash_participant(request):
    if request.method == "POST":
        User = get_user_model()
        try:
            data = json.loads(request.body)
            flash_id = data.get("flash_id")
            user_id = data.get("user_id")

            flash = get_object_or_404(Flash, meeting_id=flash_id)
            user = get_object_or_404(User, id=user_id)

            # 참가자 삭제
            deleted_count, _ = FlashParticipants.objects.filter(flash=flash, user=user).delete()
            
            if deleted_count > 0:  # ✅ 실제로 삭제된 경우만 now_member 감소
                flash.now_member = max(flash.now_member - 1, 0)  # 음수 방지
                flash.save()

            # 참가 요청도 삭제
            FlashRequest.objects.filter(flash=flash, user=user).delete()

            # 최신 참가자 리스트 다시 가져오기
            participant_ids = list(FlashParticipants.objects.filter(flash=flash).values_list("user_id", flat=True))

            return JsonResponse({
                "message": "참가 취소!",
                "participant_ids": participant_ids  # ✅ 최신 참가자 리스트 반환
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@login_required
def apply_flash_participant(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            flash_id = data.get("flash_id")
            flash = Flash.objects.get(meeting_id=flash_id)

            # 중복 참가 방지
            if FlashParticipants.objects.filter(flash=flash, user=request.user).exists():
                return JsonResponse({"success": False, "message": "이미 참가 중입니다."}, status=400)

            # 중복 참가 요청 방지
            if FlashRequest.objects.filter(flash=flash, user=request.user).exists():
                return JsonResponse({"success": False, "message": "이미 참가 요청을 보냈습니다."}, status=400)

            # 참가자 추가 요청
            FlashRequest.objects.create(flash=flash, user=request.user)

            return JsonResponse({"success": True, "message": "참가 신청이 완료되었습니다!"})
        except Flash.DoesNotExist:
            return JsonResponse({"success": False, "message": "해당 번개를 찾을 수 없습니다."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "잘못된 요청입니다."}, status=400)

@csrf_exempt
@login_required
def cancel_flash_participant(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            flash_id = data.get("flash_id")
            flash = Flash.objects.get(meeting_id=flash_id)

            # 참가 신청 취소
            FlashRequest.objects.filter(flash=flash, user=request.user).delete()

            return JsonResponse({"success": True, "message": "참가 신청이 취소되었습니다."})
        except Flash.DoesNotExist:
            return JsonResponse({"success": False, "message": "해당 번개를 찾을 수 없습니다."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "잘못된 요청입니다."}, status=400)

@login_required
def get_flash_requests(request, flash_id):

    flash = get_object_or_404(Flash, meeting_id=flash_id)

    if request.user != flash.created_by:
        return JsonResponse({"error": "권한이 없습니다."}, status=403)

    requests = FlashRequest.objects.filter(flash=flash).select_related("user")
    request_list = [{"id": r.user.id, "email": r.user.email} for r in requests]

    return JsonResponse({"success": True, "requests": request_list})
