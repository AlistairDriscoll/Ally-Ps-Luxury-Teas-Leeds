from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path(
        "with_sample/<int:tea_pk>/",
        views.checkout_with_sample,
        name="checkout_with_sample"
    ),
    path(
        "checkout_success/<order_number>/",
        views.checkout_success,
        name="checkout_success",
    ),
]
