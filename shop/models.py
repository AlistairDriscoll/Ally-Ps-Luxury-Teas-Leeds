import uuid

from django.db import models


def generate_sku():
    return str(uuid.uuid4().hex[:8]).upper()  # Example SKU: "A1B2C3D4"


class Product(models.Model):
    """
    Model for the tea products
    """

    TYPES = ((0, "Black"), (1, "Green"), (2, "Herbal"))

    name = models.CharField(max_length=65)
    sku = models.CharField(
        max_length=8,
        unique=True,
        default=generate_sku,
    )

    tea_type = models.IntegerField(choices=TYPES, default=0)
    base_price_number = models.DecimalField(max_digits=4, decimal_places=2)
    picture = models.ImageField(
        upload_to="products/",
        blank=True,
        default='camellia-sinensis.jpg'
    )

    def __str__(self):
        return self.name
