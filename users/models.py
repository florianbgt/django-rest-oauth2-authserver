from django.db import models
from django.contrib.auth.models import AbstractUser     #new
from .managers import CustomUserManager     #new


class CustomUser(AbstractUser):     #new
    username = None     #new
    first_name = None       #new
    last_name = None        #new
    email = models.EmailField(max_length=50, unique=True)     #new

    USERNAME_FIELD = 'email'     #new
    REQUIRED_FIELDS = []       #new

    objects = CustomUserManager()       #new

    def __str__(self):      #new
        return self.email       #new