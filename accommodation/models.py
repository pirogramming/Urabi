from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AccommodationReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accommodation_reviews")  # 작성자 ID
    city = models.CharField(max_length=50)  # 숙소 위치 도시
    accommodation_name = models.CharField(max_length=100)  # 숙소명
    category = models.CharField(max_length=50)  # 숙소 유형
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # 평점 (1.0 ~ 5.0)
    content = models.TextField(null=True, blank=True)  # 후기 내용 (nullable)
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일
    photo = models.ImageField(upload_to="accommodation_reviews/", null=True, blank=True)  # 후기 사진
    is_parent = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.accommodation_name} ({self.rating}⭐)"
    
    
class ReviewComment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    review = models.ForeignKey(AccommodationReview, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_comment'

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.accommodation_name}"