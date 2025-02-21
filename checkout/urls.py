from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("payment/<int:order_id>", views.payment, name="payment"),
]
