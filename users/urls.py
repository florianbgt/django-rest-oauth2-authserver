from django.urls import path        #new
from .views import SignUp, PasswordChange        #new


urlpatterns = [        #new
    path('signup/', SignUp.as_view()),
    path('password/', PasswordChange.as_view()),        #new
]        #new