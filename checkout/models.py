import uuid

from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from profiles.models import UserProfile
from shop.models import Product

from django_countries.fields import CountryField

DELIVERY_CHOICES = [3, 7, 15]


def validate_delivery_cost(value):
    """Makes sure delivery cost is right"""
    if value not in DELIVERY_CHOICES:
        raise ValidationError(
                f"Delivery cost must be {DELIVERY_CHOICES}. Given: {value}"
            )


class Order(models.Model):
    """
    SET_NULL will set the user_profile the null but keep the rest of the order
    so it stays on record
    null and blank = true so that the user doesn't need an account to create
    orders
    Adapted from Code Institute's Order model
    """

    def _send_confirmation_email(self):
        """
        Sends the user a confirmation email
        Taken and adapted from code institute
        """
        cust_email = self.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': self},
        )
        body = render_to_string(
            "checkout/confirmation_emails/confirmation_email_body.txt",
            {"order": self, "default_from_email": settings.DEFAULT_FROM_EMAIL},
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    order_number = models.CharField(max_length=32, null=False, editable=False)

    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    state_or_region = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label="Country *", null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.IntegerField(
        default=3,
        validators=[validate_delivery_cost]
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    original_bag = models.TextField(blank=False, null=False, default="")

    def _generate_order_number(self):
        """
        Generate a random, unique order number using uuid
        Taken from Code Institute Boutique Ado walkthrough
        """

        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Calculates the new total whenever a new OrderItem is made"""

        self.order_total = (
            self.lineitems.aggregate(
                Sum("item_total")).get("item_total__sum", 0)
            or 0
        )

        self.grand_total = self.order_total + self.delivery_cost

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        If it hasn't been set already
        """

        if not self.order_number:
            self.order_number = self._generate_order_number()

        if not self.pk:
            self._send_confirmation_email()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    """
    Model for each item added to the order
    Taken from Code Institute Boutique Ado walkthrough
    """

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='product'
    )
    weight = models.CharField(max_length=3, blank=True, default=30)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    item_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False
    )

    def calculate_cost(self, weight, base_price):
        if weight == 5:
            return 0
        elif weight == 30:
            return base_price
        elif weight == 100:
            return base_price * 3
        elif weight == 300:
            return base_price * 8
        else:
            return base_price

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        And update the order total
        """

        self.item_total = self.calculate_cost(
            self.weight, self.product.base_price_number
        ) * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
