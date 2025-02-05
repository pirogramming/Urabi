from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Flash, FlashZzim
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import F

def flash_list(request):
    flash_meetings = Flash.objects.all().order_by("-created_at")

    # 태그를 리스트로 변환하여 flash_meetings에 추가
    for flash in flash_meetings:
        flash.tag_list = flash.tags.split(",") if flash.tags else []
        flash.image_url = f"https://maps.googleapis.com/maps/api/streetview?size=500x500&location={flash.latitude},{flash.longitude}&key=AIzaSyDZLQne-DOUQDfifh3ZP_79TmL2OmBOI7k"
    return render(request, "flash/flash_list.html", {"flash_meetings": flash_meetings})

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

    return render(request, "flash/flash_register.html")

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

    # 현재 번개와 가장 가까운 2개의 번개 찾기 (pk 기준으로 가장 가까운 번개)
    other_flash_meetings = Flash.objects.exclude(pk=pk).order_by(F('pk') - pk)[:2]

    if flash.latitude and flash.longitude:
        place_img_url = f"https://maps.googleapis.com/maps/api/streetview?size=500x500&location={flash.latitude},{flash.longitude}&key=AIzaSyDZLQne-DOUQDfifh3ZP_79TmL2OmBOI7k"
    else:
        place_img_url = "https://via.placeholder.com/300"

    # 다른 번개들도 이미지 URL 설정
    for other_flash in other_flash_meetings:
        if other_flash.latitude and other_flash.longitude:
            other_flash.image_url = f"https://maps.googleapis.com/maps/api/streetview?size=500x500&location={other_flash.latitude},{other_flash.longitude}&key=AIzaSyDZLQne-DOUQDfifh3ZP_79TmL2OmBOI7k"
        else:
            other_flash.image_url = "https://via.placeholder.com/300"

    return render(request, "flash/flash_detail.html", {"flash": flash, "tag_list": tag_list,"is_zzimmed": is_zzimmed,'place_img_url': place_img_url, "other_flash_meetings": other_flash_meetings})



@login_required
def flash_zzim(request, pk):

    flash = get_object_or_404(Flash, pk=pk)
    user = request.user

    zzim, created = FlashZzim.objects.get_or_create(user=user, flash=flash)

    if not created:
        zzim.delete()  # 이미 찜한 경우 삭제
        return JsonResponse({"zzimmed": False})
    
    return JsonResponse({"zzimmed": True})
