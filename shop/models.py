from django.db import models


class Product(models.Model):
    """
    Model for the tea products
    """

    TYPES = ((0, "Black"), (1, "Green"), (2, "Herbal"))

    name = models.CharField(max_length=65)
    type = models.IntegerField(choices=TYPES, default=0)
    base_price_number = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name
