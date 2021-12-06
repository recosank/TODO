from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import todo_view





urlpatterns = [
    path('td/all',todo_view.as_view(),name='td'),
    path('td',todo_view.as_view(),name='td_p'),
    path("td/update/<int:pk>",todo_view.as_view(),name="update"),
    path('td/delete/<int:pk>',todo_view.as_view(),name='delete')
    
]