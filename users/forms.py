from django.contrib.auth.forms import UserCreationForm, UserChangeForm      #new
from .models import CustomUser      #new


class CustomUserCreationForm(UserCreationForm):     #new
    class Meta:     #new
        model = CustomUser      #new
        fields = ('email',)     #new


class CustomUserChangeForm(UserChangeForm):     #new
    class Meta:     #new
        model = CustomUser      #new
        fields = ('email',)     #new