from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        extra_fields.setdefault('is_active', True)  

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
    username = None
    user_age = models.IntegerField(null=True, blank=True)  
    user_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    user_phone = models.CharField(max_length=20)
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
