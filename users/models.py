from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일을 입력해야 합니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=50)
    user_age = models.PositiveIntegerField()
    user_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    user_phone = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    trust_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'user_age', 'user_gender', 'user_phone', 'nickname']

    def __str__(self):
        return self.email