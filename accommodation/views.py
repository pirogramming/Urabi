from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AccommodationReview
from django.contrib import messages
from django.db.models import Subquery, OuterRef, Max
from django.db.models import Avg

def accommodation_filter(request):
    """메인페이지"""
    # 검색 파라미터 가져오기
    city_query = request.GET.get('city', '')
    rating_query = request.GET.get('rating', '')
    
    # 각 숙소별 최신 리뷰를 가져오는 서브쿼리
    latest_reviews = AccommodationReview.objects.filter(
        accommodation_name=OuterRef('accommodation_name')
    ).order_by('-created_at')
    
    # 기본 쿼리셋 (최신 리뷰만 포함)
    reviews = AccommodationReview.objects.filter(
        review_id=Subquery(
            latest_reviews.values('review_id')[:1]
        )
    )

    # 검색 필터링 적용
    if city_query:
        reviews = reviews.filter(city__icontains=city_query)

    if rating_query:
        try:
            min_rating = float(rating_query)
            reviews = reviews.filter(rating__gte=min_rating)
        except ValueError:
            pass

    # 최종 정렬
    reviews = reviews.order_by('-created_at')
    
    context = {
        'reviews': reviews,
        'city_query': city_query,  
        'rating_query': rating_query  
    }
    
    return render(request, "accommodation/accommodation_filter.html", context)


def accommodation_location(request):
    """숙소 위치를 지도에서 보여주는 페이지"""
    # 각 숙소의 최신 리뷰만 가져오기
    latest_reviews = AccommodationReview.objects.filter(
        accommodation_name=OuterRef('accommodation_name')
    ).order_by('-created_at')
    
    reviews = AccommodationReview.objects.filter(
        review_id=Subquery(
            latest_reviews.values('review_id')[:1]
        )
    ).order_by('-created_at')
    
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
    # 메인 리뷰 가져오기
    review = get_object_or_404(AccommodationReview.objects.select_related('user'), pk=pk)
    
    # 같은 숙소의 모든 리뷰들 가져오기 (현재 리뷰 포함)
    all_reviews = AccommodationReview.objects.select_related('user').filter(
        accommodation_name=review.accommodation_name
    ).order_by('-created_at')
    
    # 리뷰 개수 계산
    review_count = all_reviews.count()
    
    # 평균 평점 계산
    average_rating = AccommodationReview.objects.filter(
        accommodation_name=review.accommodation_name
    ).aggregate(avg_rating=Avg('rating'))['avg_rating']
    
    if average_rating:
        average_rating = round(average_rating, 1)
    
    return render(request, "accommodation/accommodation_reviewdetail.html", {
        "review": review,
        "all_reviews": all_reviews,
        "average_rating": average_rating,
        "review_count": review_count 
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
