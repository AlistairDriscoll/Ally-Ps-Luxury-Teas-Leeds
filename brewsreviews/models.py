from django.db import models
from django.utils import timezone

from shop.models import Product


class BlogPost(models.Model):
    """Blog post class"""

    title = models.CharField(max_length=100, blank=True, null=False)
    tea = models.OneToOneField(
        Product, on_delete=models.PROTECT, related_name="blog_post"
    )
    date_added = models.DateTimeField(
        auto_now_add=True
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
        """
        If user doesn't assign a title, assign it the same name as the tea.
        If user doesn't assign a tea, make title its created on date.
        """
        if not self.title:
            if self.tea:
                self.title = self.tea.name
            else:
                self.title = timezone.now().strftime("%Y-%m-%d")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
