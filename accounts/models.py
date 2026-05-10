from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    language_preference = models.CharField(max_length=10, default='en')
    saved_destinations = models.ManyToManyField('cities.City', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
