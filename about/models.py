from django.db import models


class Enquiry(models.Model):
    """Enquiry model for users to send emails"""

    email = models.EmailField(blank=False, null=True)
    subject = models.CharField(blank=False, null=True, max_length=50)
    content = models.TextField(blank=False, null=True)
