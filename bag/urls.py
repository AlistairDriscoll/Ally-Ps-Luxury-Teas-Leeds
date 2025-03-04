from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:product_id>/", views.add_to_bag, name="add_to_bag"),
    path("edit/<int:product_id>/", views.edit_bag, name="edit_bag"),
    path(
        "delete/<int:product_id>/<int:weight>/",
        views.delete_from_bag,
        name="delete_from_bag",
    ),
    path("", views.view_bag, name="view_bag"),
]
