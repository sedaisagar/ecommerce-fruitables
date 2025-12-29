from datetime import datetime, timedelta
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from users.user_manager import CustomUserManager
from utils.models import BaseModel


class User(AbstractUser):
    ROLES = (
        ("ADMIN", "ADMIN"),
        ("CUSTOMER","CUSTOMER")
    )
    role = models.CharField(choices=ROLES, max_length=8, default="CUSTOMER")
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "auth_users"



class UserOtp(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_otp")

    # Allows for maximum of 6 digits with no decimal values
    otp = models.DecimalField(max_digits=6, decimal_places=0) 
    
    @property
    def is_expired(self):
        cond_time = self.created_at + timedelta(minutes=2)
        return cond_time < datetime.now()
            
    class Meta:
        db_table = "user_otps"
