from django.db import models
from django.utils import timezone
from V1.App1.models import custom_user

class profile(models.Model):
    user = models.OneToOneField(custom_user,on_delete=models.CASCADE,related_name="user_profile")
    
    img = models.ImageField(upload_to="V1/App2/static/images")
    date_created= models.DateTimeField( default=timezone.now)

    def __str__(self) -> str:
        return self.user.username
