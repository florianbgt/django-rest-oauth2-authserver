from rest_framework import generics     #new
from rest_framework.permissions import AllowAny     #new
from django.contrib.auth import get_user_model     #new
from .serializers import SignUpSerializer, PasswordChangeSerializer     #new

User = get_user_model()     #new


class SignUp(generics.CreateAPIView):       #new
    permission_classes = [AllowAny]       #new
    serializer_class = SignUpSerializer       #new


class PasswordChange(generics.UpdateAPIView):     #new
    queryset = User     #new
    serializer_class = PasswordChangeSerializer     #new
    def get_object(self):     #new
        return self.request.user     #new