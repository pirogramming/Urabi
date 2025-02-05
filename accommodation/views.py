from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AccommodationReview
from django.contrib import messages

def accommodation_filter(request):
    """메인페이지"""
    # 숙소별로 가장 최근 리뷰만 가져오기
    from django.db.models import Max
    
    # 각 숙소별 최신 리뷰의 ID를 찾기 
    latest_reviews = AccommodationReview.objects.values('accommodation_name').annotate(
        latest_id=Max('review_id')
    )
    
    # 최신 리뷰 ID 추출
    latest_review_ids = [item['latest_id'] for item in latest_reviews]
    
    # 해당 ID의 리뷰들 가져오기 
    reviews = AccommodationReview.objects.filter(
        review_id__in=latest_review_ids
    ).order_by('-created_at')
    
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
    # 같은 숙소의 다른 후기들 가져오기
    related_reviews = AccommodationReview.objects.filter(
        accommodation_name=review.accommodation_name
    ).exclude(pk=review.pk).order_by('-created_at')
    
    return render(request, "accommodation/accommodation_reviewdetail.html", {
        "review": review,
        "related_reviews": related_reviews
    })

@login_required
def accommodation_review_create(request, pk):
    """특정 숙소의 후기 작성 페이지"""
    parent_review = get_object_or_404(AccommodationReview, pk=pk)
    
    if request.method == "POST":
        try:
            review = AccommodationReview(
                user=request.user,
                city=parent_review.city,
                accommodation_name=parent_review.accommodation_name,
                category=parent_review.category,
                rating=float(request.POST.get('rating')),
                content=request.POST.get('content')
            )
            if 'photo' in request.FILES:
                review.photo = request.FILES['photo']
            review.save()
            messages.success(request, '후기가 성공적으로 등록되었습니다.')
            return redirect('accommodation:accommodation_review_detail', pk=pk)
        except Exception as e:
            messages.error(request, f'후기 등록 중 오류가 발생했습니다: {str(e)}')
    
    return render(request, "accommodation/accommodation_reviewcreate.html", {
        "parent_review": parent_review
    })
