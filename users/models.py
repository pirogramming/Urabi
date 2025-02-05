from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        extra_fields.setdefault('is_active', True) 

        if not extra_fields.get('nickname'):
            extra_fields['nickname'] = extra_fields.get('username', '') 

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    user_age = models.IntegerField(null=True, blank=True)  
    user_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True, default=None) # 오류땜에 잠깐 바꿈
    user_phone = models.CharField(max_length=20, null=True, blank=True, default=None) # 오류땜에 잠깐 바꿈
    nickname = models.CharField(max_length=50, null=True)
    birth = models.DateField(null=True, blank=True)
    social_id = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True, default='profile_images/default-profile.png')
    trust_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

class TravelPlan(models.Model):
    plan_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)  # 일정 제목
    city = models.CharField(max_length=50)  # 도시명
    explanation = models.TextField()  # 일정 설명
    start_date = models.DateField()  # 시작 날짜
    end_date = models.DateField()  # 종료 날짜
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_plans')  # 작성자
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 마커와 폴리라인 데이터를 저장할 필드
    markers = models.JSONField(null=True, blank=True)  
    polyline = models.JSONField(null=True, blank=True)  
        # 공개 여부를 저장할 필드 (기본값은 비공개)
    is_public = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.title} - {self.created_by.username}"