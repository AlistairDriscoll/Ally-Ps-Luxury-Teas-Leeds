from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    A basic UserProfile model for user's data storage
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
