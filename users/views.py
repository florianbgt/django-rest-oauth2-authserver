
from rest_framework import generics     #new
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model     #new
from .serializers import SignUpSerializer, PasswordChangeSerializer     #new

User = get_user_model()     #new


class SignUp(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer


class PasswordChange(generics.UpdateAPIView):     #new
    queryset = User     #new
    serializer_class = PasswordChangeSerializer     #new
    def get_object(self):     #new
        return self.request.user     #new