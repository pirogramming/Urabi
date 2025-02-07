from django.db import models
from users.models import User
from django.conf import settings 

# Create your models here.
class Market(models.Model):
    TRADE_TYPE_CHOICES = [
        ('판매', '🛒 판매해요' ),
        ('구매', '🛍️ 구매해요' ),
        ('나눔', '🎁 나눔해요' ),
    ]

    CATEGORY_CHOICES = [
        ('의약품', '#의약품' ),
        ('티켓', '#티켓' ),
        ('음식', '#음식' ),
        ('생활용품', '#생활용품' ),
        ('기념품', '#기념품' ),
        ('기타', '#기타' ),
    ]

    TRADE_STATUS_CHOICES = [
        ('거래 가능', '거래 가능' ),
        ('거래 완료', '거래 완료' ),
        ('예약', '예약' ),
    ]

    item_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name=("작성자"), on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=10, choices=TRADE_TYPE_CHOICES)
    city = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    explanation = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='거래 가능', choices=TRADE_STATUS_CHOICES)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    photo = models.ImageField('마켓_이미지', blank=True, upload_to='market/%Y%m%d')

    def __str__(self):
        return f"{self.get_trade_type_display()}-{self.title} ({self.city})"
    
class MarketZzim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "market")  # 중복 찜 방지
    
    def __str__(self):
        return f"{self.user} : {self.market.title}"


