from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AccommodationReview
from django.contrib import messages

def accommodation_filter(request):
    """메인페이지"""
    reviews = AccommodationReview.objects.all().order_by('-created_at')
    return render(request, "accommodation/accommodation_filter.html", {'reviews': reviews})

def accommodation_location(request):
    """숙소 위치를 지도에서 보여주는 페이지"""
    reviews = AccommodationReview.objects.all()
    return render(request, "accommodation/accommodation_location.html", {"reviews": reviews})

@login_required
def accommodation_create(request):
    """숙소 후기 작성 페이지"""
    if request.method == "POST":
        try:
            review = AccommodationReview(
                user=request.user,
                city=request.POST.get('city'),
                accommodation_name=request.POST.get('accommodation_name'),
                category=request.POST.get('category'),
                rating=float(request.POST.get('rating')),
                content=request.POST.get('content')
            )
            if 'photo' in request.FILES:
                review.photo = request.FILES['photo']
            review.save()
            messages.success(request, '후기가 성공적으로 등록되었습니다.')
            return redirect('accommodation:filter')
        except Exception as e:
            messages.error(request, f'후기 등록 중 오류가 발생했습니다: {str(e)}')
    return render(request, "accommodation/accommodation_create.html")

def accommodation_review_detail(request, pk):
    """숙소 후기 상세 조회 페이지"""
    review = get_object_or_404(AccommodationReview, pk=pk)
    return render(request, "accommodation/accommodation_reviewdetail.html", {"review": review})
