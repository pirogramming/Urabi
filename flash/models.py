from django.db import models
from django.conf import settings 

class Flash(models.Model):
    meeting_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=50, null=False)
    # 지도 api 받아오기 전까지 임시로 null blank 처리
    latitude = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    date_time = models.DateTimeField(null=False)
    max_people = models.IntegerField(null=False)
    explanation = models.TextField(null=False)
    tags = models.TextField(blank=True)  # 태그 저장 (쉼표로 구분된 문자열)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class FlashZzim(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flash = models.ForeignKey(Flash, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "flash")  # 중복 찜 방지

