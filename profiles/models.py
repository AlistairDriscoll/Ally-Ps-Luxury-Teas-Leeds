from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A basic UserProfile model for user's data storage
    Adapted from Code Institute's Boutique Ado walkthrough
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    full_name = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    subscribed_to_email = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    town_or_city = models.CharField(max_length=120, blank=True, null=True)
    state_or_region = models.CharField(max_length=120, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s UserProfile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    Taken from Code institute's boutique ado walkthrough
    """

    if created:
        UserProfile.objects.create(user=instance)
    # existing users: just save the profile
    instance.userprofile.save()
