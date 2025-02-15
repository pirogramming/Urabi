from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

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
    user_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True, default=None)
    user_phone = models.CharField(max_length=20, null=True, blank=True, default=None) 
    nickname = models.CharField(max_length=10, null=True)
    birth = models.DateField(null=True, blank=True)
    social_id = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True, default='profile_images/default-profile.png')
    trust_score = models.IntegerField(default=36.5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()


class TravelSchedule(models.Model):
    schedule_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)            # 일정 이름 (필수)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='travel_schedules')
    start_date = models.DateField()  # 시작 날짜
    end_date = models.DateField()  # 종료 날짜
    photo = models.ImageField(upload_to='schedule_images', null=True, blank=True)
    is_public = models.BooleanField(default=False)  # 필요하다면 사용

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.nickname}"

class TravelPlan(models.Model):
    plan_id    = models.BigAutoField(primary_key=True)
    schedule   = models.ForeignKey(TravelSchedule, on_delete=models.CASCADE, related_name='plans')
    explanation = models.TextField()  
    start_date = models.DateField()  
    end_date = models.DateField()  
    markers = models.JSONField(null=True, blank=True)
    polyline = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_plans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plan #{self.plan_id} for {self.schedule.name}"
    
class PhoneVerification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    random_string = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.random_string