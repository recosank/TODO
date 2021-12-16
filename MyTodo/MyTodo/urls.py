from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("v1/",include("V1.App1.urls")),
    path("v1/",include("V1.App2.urls")),
    path("v2/",include("V2.App3.urls"))
]
