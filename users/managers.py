from django.contrib.auth.base_user import BaseUserManager       #new


class CustomUserManager(BaseUserManager):       #new
    def create_user(self, email, password, **extra_fields):       #new
        if not email:       #new
            raise ValueError('The Email must be set')       #new
        email = self.normalize_email(email)       #new
        user = self.model(email=email, **extra_fields)       #new
        user.set_password(password)       #new
        user.save()       #new
        return user       #new

    def create_superuser(self, username, email, password, **extra_fields):       #new
        extra_fields.setdefault('is_staff', True)       #new
        extra_fields.setdefault('is_superuser', True)       #new
        extra_fields.setdefault('is_active', True)       #new
        if extra_fields.get('is_staff') is not True:       #new
            raise ValueError('Superuser must have is_staff=True.')       #new
        if extra_fields.get('is_superuser') is not True:       #new
            raise ValueError('Superuser must have is_superuser=True.')       #new
        return self.create_user(email, password, **extra_fields)       #new