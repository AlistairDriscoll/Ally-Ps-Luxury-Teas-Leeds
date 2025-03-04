from django.db import models
from shop.models import Product


class BlogPost(models.Model):
    """Blog post class"""

    title = models.CharField(max_length=100, blank=False)
    tea = models.OneToOneField(
        Product, on_delete=models.PROTECT, related_name="blog_post"
    )
    content = models.TextField()
