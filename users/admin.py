from django.contrib import admin
from django.contrib.auth.admin import UserAdmin     #new

from .forms import CustomUserCreationForm, CustomUserChangeForm     #new
from .models import CustomUser     #new


class CustomUserAdmin(UserAdmin):     #new
    add_form = CustomUserCreationForm     #new
    form = CustomUserChangeForm     #new
    model = CustomUser     #new
    list_display = ('email', 'is_staff', 'is_active',)     #new
    list_filter = ('email', 'is_staff', 'is_active',)     #new
    fieldsets = (     #new
        ('Credentials', {'fields': ('email', 'password')}),     #new
        ('User informations', {'fields': ('first_name', 'last_name')}),     #new
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),     #new
    )     #new
    add_fieldsets = (     #new
        (None, {     #new
            'classes': ('wide',),     #new
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}     #new
        ),     #new
    )     #new
    search_fields = ('email',)     #new
    ordering = ('email',)     #new


admin.site.register(CustomUser, CustomUserAdmin)     #new