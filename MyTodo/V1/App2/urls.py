from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import p_v

urlpatterns = [
    
    path('p',p_v.as_view(),name="profile"),

]