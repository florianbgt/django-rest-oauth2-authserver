
from rest_framework import generics     #new
from django.contrib.auth import get_user_model     #new
from .serializers import ProfileChangeSerializer, PasswordChangeSerializer     #new

User = get_user_model()     #new

class ProfileChange(generics.RetrieveUpdateAPIView):     #new
    queryset = User     #new
    serializer_class = ProfileChangeSerializer     #new
    def get_object(self):     #new
        return self.request.user     #new

class PasswordChange(generics.UpdateAPIView):     #new
    queryset = User     #new
    serializer_class = PasswordChangeSerializer     #new
    def get_object(self):     #new
        return self.request.user     #new