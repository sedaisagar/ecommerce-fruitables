from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from users.user_manager import CustomUserManager


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
