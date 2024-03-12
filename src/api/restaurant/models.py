from django.db import models
import django.utils.timezone as timezone
from django.contrib.auth.models import User


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    title = models.CharField(max_length=64, null=False, default='')
    content = models.TextField(null=False, default='')
    score = models.PositiveIntegerField(default=0)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', default='')
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ('restaurant_id', 'user_id',)
    