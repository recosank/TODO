from django.urls import path
from .views import p_v

urlpatterns = [
    path('p',p_v.as_view(),name="profile"),

]