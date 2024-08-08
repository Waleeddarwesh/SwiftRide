from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from .manager import UserManager
from django.contrib.auth.hashers import make_password

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False)    
    email = models.EmailField(max_length=255, verbose_name=_("Email Address"), unique=True)
    username = models.CharField(max_length=100, unique=True)
    user_photo =models.ImageField(upload_to='user_photos/%y/%m/%d',blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    last_password_reset_request = models.DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ["username","password"]
    objects = UserManager()
    USERNAME_FIELD = "email"

    def tokens(self):   
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
     if not self.pk or not self.password:
        if not self.pk:
            self.pk = None
        self.password = make_password(self.password)
     super().save(*args, **kwargs)

class OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.email} - otp code"
