import random
from django.contrib.auth import authenticate
from .models import custom_user
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import settings
from .token import get_tokens_for_user

def create_username(name):
    us = "".join(name.split(" ").lower())
    if not custom_user.objects.filter(username=us).exists():
        return us
    r_name = us + str(random.randint(0,1000))
    return create_username(r_name)

def create_social_user(p,u_id,u,e):
    us = custom_user.objects.filer(email=e)
    if us.exists():
        if us[0].auth_provider == p:
            a_user = authenticate(user=us,password=settings['SOCIAL_SECREAT'])
            u_token = get_tokens_for_user(a_user)
            return {
                'username': a_user.username,
                'email': a_user.email,
                'tokens': u_token}
        raise AuthenticationFailed("login with " + us[0].auth_provider)

    user = {"username":create_username(u),'email':e,"password":settings['SOCIAL_SECREAT','is_verified':True,'auth_provider':p]}
    u = custom_user.objects.create_user(**user)
    u.save()
    a_user = authenticate(user=us,password=settings['SOCIAL_SECREAT'])
    u_token = get_tokens_for_user(a_user)
    return {
                'username': a_user.username,
                'email': a_user.email,
                'tokens': u_token
    }

