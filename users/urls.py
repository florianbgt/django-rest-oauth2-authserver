from django.urls import path        #new
from .views import ProfileChange, PasswordChange        #new


urlpatterns = [        #new
    path('profile/', ProfileChange.as_view()),        #new
    path('password/', PasswordChange.as_view()),        #new
]        #new