from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AccommodationReview

def accommodation_filter(request):
    """메인페이지"""
    return render(request, "accommodation/accommodation_filter.html")

def accommodation_location(request):
    """숙소 위치를 지도에서 보여주는 페이지"""
    reviews = AccommodationReview.objects.all()
    return render(request, "accommodation/accommodation_location.html", {"reviews": reviews})

def accommodation_create(request):
    """숙소 후기 작성 페이지"""
    return render(request, "accommodation/accommodation_create.html")

def accommodation_review_detail(request, pk):
    """숙소 후기 상세 조회 페이지"""
    review = get_object_or_404(AccommodationReview, pk=pk)
    return render(request, "accommodation/accommodation_reviewdetail.html", {"review": review})
