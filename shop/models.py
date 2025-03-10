import uuid
import os

from django.db import models

from cloudinary.models import CloudinaryField


def generate_sku():
    """
    Generate a unique SKU for the product.
    """
    while True:
        new_sku = str(uuid.uuid4().hex[:8]).upper()  # Example SKU: "A1B2C3D4"
        if not Product.objects.filter(sku=new_sku).exists():
            return new_sku


def product_image_upload_path(instance, filename):
    """
    Generate file path for new product image,
    storing it in a folder named after the SKU.
    """

    return os.path.join("products", instance.sku, filename)


class Product(models.Model):
    """
    Model for the tea products
    """

    TYPES = ((0, "Black"), (1, "Green"), (2, "Herbal"))
    ORIGINS = (
        ("China", "China"),
        ("India", "India"),
        ("Japan", "Japan"),
        ("Sri Lanka", "Sri Lanka"),
        ("Kenya", "Kenya"),
        ("Others", "Others"),
        )

    FLAVOR_PROFILES = (("Floral", "Floral"),
                       ("Fruity", "Fruity"),
                       ("Earthy", "Earthy"),
                       ("Malty", "Malty"),
                       ("Others", "Others"),)

    CAFFEINE_LEVELS = (("High", "High"),
                       ("Medium", "Medium"),
                       ("Low", "Low"),
                       ("Caffeine-Free", "Caffeine-Free"),)

    name = models.CharField(max_length=65)
    sku = models.CharField(
        max_length=8,
        unique=True,
        default=generate_sku,
    )

    tea_type = models.IntegerField(choices=TYPES, default=0)
    origin = models.CharField(max_length=20, choices=ORIGINS, default="Others")
    flavor_profile = models.CharField(
        max_length=20, choices=FLAVOR_PROFILES, default="Others"
        )
    caffeine_level = models.CharField(
        max_length=20, choices=CAFFEINE_LEVELS, default="Medium"
        )
    base_price_number = models.DecimalField(max_digits=4, decimal_places=2)
    picture = CloudinaryField(
        default='placeholder',
        blank=True,
    )

    def __str__(self):
        return self.name
