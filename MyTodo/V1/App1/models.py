from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.dispatch import receiver
from django.urls import reverse

class custom_manager(BaseUserManager):
    def user_save(self,username,password,email,**kwargs):
        if username is None: 
            raise AttributeError('username not defined')
                    
        email = self.normalize_email(email)
        user = self.model(username = username,email=email,**kwargs)
        user.set_password(password)
        user.save(using = self.db)
        return user
    
    def create_user(self,username,password,email,**extra):
        if email is None:
            raise TypeError('Users should have a Email')
        email=self.normalize_email(email)
        extra['is_superuser'] = False
        extra['is_staff'] = False
        return self.user_save(username,password,email,**extra)

    def create_staffuser(self,username,password,**extra):
        extra['is_superuser'] = False
        extra['is_staff'] = True
        extra['is_active'] = False
        return self.user_save(username,password,**extra)


    def create_superuser(self,username,password,**extra):
        extra['is_superuser'] = True
        extra.setdefault('is_superuser',True)
        if extra.get('is_superuser') is not True :
            raise ValueError("not valid u r lier")
        extra['is_staff'] = True
        return self.user_save(username,password,**extra)

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

class custom_user(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=254)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email']
    objects = custom_manager()
    def __str__(self):
        return self.username
  
    