from django.contrib import admin
from django.urls import path, include       #new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),       #new
    path('users/', include('users.urls'))        #new
]
