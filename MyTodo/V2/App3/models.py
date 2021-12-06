from django.db import models
from django.utils import timezone
from V1.App2.models import profile

class td(models.Model):
    user = models.ForeignKey(profile,on_delete=models.CASCADE,related_name="todo")
    task = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    
    is_pending = models.BooleanField(default=False)

    class Meta:
        ordering = ('-is_pending','date_created')

    def __str__(self):
        return self.user.user.username
