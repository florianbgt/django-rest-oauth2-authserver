---
title: Django REST Oauth2 SSO authentication server
description: Oauth2 SSO authentication server implementation with the Django REST framework and the Django OAuth Toolkit library
image: 
---

In this article, I will show you how to setup

## 1) Setting up our project
In this section, we will setup our Django project and customize the default user model to implement email authentication

First, we create our virtual environement:
```bash
mkdir Django-rest-oauth2-auth-server
cd Django-rest-oauth2-auth-server
python -m venv env
### if you arer using Windows
env\scripts\activate
### if you are using Mac or Linux
source env/bin/activate
```

We then install django and create our project:
```bash
pip install django
django-admin startproject _project .
```

To implement email authentication, we create a new app and add 2 nrew files:
```bash
python manage.py startapp users
touch users/managers.py
touch users/forms.py
```

The first thing we need a custom manager.   
For that, we simply extend django BaseUserManager and define the create_user and create_superuser methods (see https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model):
```python
### users/managers.py
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

    def create_superuser(self, email, password, **extra_fields):       #new
        extra_fields.setdefault('is_staff', True)       #new
        extra_fields.setdefault('is_superuser', True)       #new
        extra_fields.setdefault('is_active', True)       #new
        if extra_fields.get('is_staff') is not True:       #new
            raise ValueError('Superuser must have is_staff=True.')       #new
        if extra_fields.get('is_superuser') is not True:       #new
            raise ValueError('Superuser must have is_superuser=True.')       #new
        return self.create_user(email, password, **extra_fields)       #new
```

We then define our custom user model   
Here, we extend django default user model using the AbstractUser:
- We set the username to None and ensure email are unique
- Then, we tell Django to use the users email for authentication using USERNAME_FIELD
- The REQUIRED_FIELDS will be the fields prompt to the user during superuser creation. If you leave it empty (what we did) the USERNAME_FIELD, password1 and password2 will be prompted. You can add any other field if needed
- Finally, tell Django to use our CustomUserManage
```python
### users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser     #new
from .managers import CustomUserManager     #new


class CustomUser(AbstractUser):     #new
    username = None
    email = models.EmailField(max_length=50, unique=True)     #new

    USERNAME_FIELD = 'email'     #new
    REQUIRED_FIELDS = []        #new

    objects = CustomUserManager()       #new

    def __str__(self):      #new
        return self.email       #new
```

As we use a custom user model, we need to customize our user model as well   

First, we need to create customized forms. In our case, we simply need to extend Django default forms and:
- Tell Django to use our custom user model
- Tell Django to use our email field instead of username
```python
### users/forms.py
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
```

We then need to includes this form into the admin using the users/admin.py file. We also need to tell Django what to display in the admin: 
```python
### users/admin.py
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
```

Finally, we add our users app to our installed apps and tell Django to use our CustomUser model
```python
### _project/settings.py
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #local
    'users',        #new
]

AUTH_USER_MODEL = 'users.CustomUser'        #new
...
```

We migrate our database and create our superuser:
```bash
python manage.py makemigrations users
python manage.py migrate
python manage.py create superuser
```

And Once all these steps done, we can spin up our dev server and make sure everything is working by going to our admin page http://localhost:8000/admin
```bash
python manage.py runserver
```

<div><blog-img src="admin_custom_user.png" alt="Django admin with custom user" width="100%" height="auto" class="shadow mb-3"/></div>

## 2) Setting up Oauth2 using Django Oauth Toolkit
In this section, we will implement a Oauth2 authentication using Django REST and Django Oauth Toolkit

First, we need to install our dependencies:
```bash
pip install djangorestframework django-oauth-toolkit django-cors-headers
```

We then:
- Add our dependencies to our app
- Add Cors middleware (need to be as high as possible, especially before CommonMiddleware)
- Define our OAuth (see https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-1-minimal-setup)
- Set REST framework authentication to OAuth toolkit one
- Set REST framework default permission to auhtenticated user
- Set cors policy to allow all. In development this setting is fine. But for production, you should set CORS_ALLOWED_ORIGINS instead (see https://pypi.org/project/django-cors-headers/)
```python
### _project/settings.py
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #local
    'users',
    #3rd party
    'corsheaders',      #new
    'rest_framework',     #new
    'oauth2_provider',      #new
]

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',        #new    #need to be as high as possible
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

OAUTH2_PROVIDER = {     #new
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60*60,       #new
    'REFRESH_TOKEN_EXPIRE_SECONDS': 24*60*60,     #new
    'SCOPES': {     #new
        'read': 'Read scope',       #new
        'write': 'Write scope',     #new
    }       #new
}       #new

REST_FRAMEWORK = {      #new
    'DEFAULT_AUTHENTICATION_CLASSES': (     #new
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',     #new
    ),     #new
    'DEFAULT_PERMISSION_CLASSES': (      #new
        'rest_framework.permissions.IsAuthenticated',      #new
    )      #new
}      #new

CORS_ALLOW_ALL_ORIGINS = True   #new        #Do not use in production 
...
```

We finally include Django OAuth Toolkit in our project urls
```python
### _project/urls.py
from django.contrib import admin
from django.urls import path, include       #new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),       #new
]
```

## 3) Create a user API
To test our OAuth implementation, we need to have API endpoints

In this section , we will create:
- One endpoint to let user change their information
- One endpoint to let user change their password

We first start by creating our serializers
```bash
touch users/serializers.py
```

```python
#users/serializers.py
from rest_framework import serializers      #new
from django.contrib.auth import get_user_model      #new
from django.contrib.auth.password_validation import validate_password       #new
from django.contrib.auth.models import Group        #new

User = get_user_model()     #new


class ProfileChangeSerializer(serializers.ModelSerializer):        #new
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')     #new

    class Meta:        #new
        model = User        #new
        depth = 1        #new
        fields = ('id', 'email', 'first_name', 'last_name', 'groups')        #new


class PasswordChangeSerializer(serializers.ModelSerializer):        #new
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])        #new
    password2 = serializers.CharField(write_only=True, required=True)       #new
    old_password = serializers.CharField(write_only=True, required=True)        #new

    class Meta:        #new
        model = User        #new
        fields = ('old_password', 'password', 'password2')        #new

    def validate_old_password(self, value):        #new
        user = self.context['request'].user        #new
        if not user.check_password(value):        #new
            raise serializers.ValidationError({'old_password': 'Old password is incorrect'})        #new
        return value        #new

    def validate(self, value):        #new
        if value['password'] != value['password2']:        #new
            raise serializers.ValidationError({'password2': 'Password fields did not match'})        #new
        return value        #new

    def update(self, instance, validated_data):        #new
        instance.set_password(validated_data['password'])        #new
        instance.save()        #new
        return instance        #new
```

Then our views
```python
### users/views.py

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
```

and finally our urls
```bash
touch users/urls.py
```

```python
### users/urls.py
from django.urls import path        #new
from .views import ProfileChange, PasswordChange        #new


urlpatterns = [        #new
    path('profile/', ProfileChange.as_view()),        #new
    path('password/', PasswordChange.as_view()),        #new
]        #new
```

```python
### _project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('user/', include('users.urls'))        #new
]
```

## 4) Test our API
To test our API, we first need to create a new client. Django OAuth Toolkit provide a nice UI to create such client here http://localhost:8000/o/applications/   
We are going to setup our application as below:
- Name: client1
- client id: clientId
- client secret clientSecret
- client type: Confidential
- Authorization grant type: Rousource owner password-based

Once done, using Postman (or curl) we can send the following http request to get our access token:
- url: http://localhost:8000/o/token/
- method: POST
- body (need to be x-www-form-urlencoded):
    - grant_type: password
    - username: user email address
    - password: user password
    - client_id: clientId
    - client_secret: clientSecret

You should get the following response (access and refresh token will be different than below):
```json
{
    "access_token": "QSonardmmRy4dZRdQlFHkmGmXIdNWf",
    "expires_in": 3600,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "zwMoXLkwXuupVpFNAlSVvB2BP8wwBF"
}
```

With our access token we can access our ressources.

Once your access token expires, you can request a new one with the refresh token. For this, we can send a POST request to the same endpoint:
- url: http://localhost:8000/o/token/
- method: POST
- body (need to be x-www-form-urlencoded):
    - grant_type: refresh_token
    - refresh_token: zwMoXLkwXuupVpFNAlSVvB2BP8wwBF
    - client_id: clientId
    - client_secret: clientSecret

You should get the following response (again, access and refresh token will be different than below):
{
    "access_token": "jIQBGaPpmI2wJboUsjlf6BxYykriBF",
    "expires_in": 3600,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "KLMePZM8WnOuv21Yz33ckdhQgRdVYn"
}

We will first try to access the user/profile/ endpoint.

But first, go to the admin page and create a group. We will name it 'group1'. Then assign this group to your user.

Let's now try to send a get request with Postman to our user/profile/ endpoint:
- url: http://localhost:8000/user/profile/
- method: GET
- Authorisation: 
    - type: Bearer Token
    - Token: jIQBGaPpmI2wJboUsjlf6BxYykriBF

You should have the following response:
```json
{
    "id": 1,
    "email": "admin@email.com",
    "first_name": "",
    "last_name": "",
    "groups": [
        "group1"
    ]
}
```

We can also modify user information (expet ID and Groups that are read only) by sending the following PUT request. Let's try to modify our first_name and last_name field!
- url: http://localhost:8000/user/profile/
- method: PUT
- Authorisation: 
    - type: Bearer Token
    - Token: jIQBGaPpmI2wJboUsjlf6BxYykriBF
- body (This time we can use JSON): {"email": "admin@email.com", "first_name": "admin", "last_name": "admin"}

You should get the following answer:
```json
{
    "id": 1,
    "email": "admin@email.com",
    "first_name": "admin",
    "last_name": "admin",
    "groups": [
        "group1"
    ]
}
```

Let's try to modify our password by seding a PUT request to our user/password/ endpoint with postman:
- url: http://localhost:8000/user/password/
- method: PUT
- Authorisation: 
    - type: Bearer Token
    - Token: jIQBGaPpmI2wJboUsjlf6BxYykriBF
- body (This time we can use JSON): {"old_password": "oldpassword", "newpassword": "oldpassword", "password2": "newpassword"}

You should receive an empty object as a response:
```json
{}
```