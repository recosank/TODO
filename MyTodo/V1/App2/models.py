from django.db import models
from django.utils import timezone
from V1.App1.models import custom_user

class profile(models.Model):
    user = models.OneToOneField(custom_user,on_delete=models.CASCADE,related_name="user_profile")
    img = models.ImageField(upload_to="V1/App2/static/images")
    bio = models.CharField(max_length=200,null=True,blank=True)
    date_created= models.DateTimeField( default=timezone.now)
    country = models.CharField(max_length=50,null=True,blank=True)
    date_of_birth = models.CharField(max_length=8,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self) -> str:
        return self.user.username
