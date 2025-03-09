from django.urls import path
from . import views

urlpatterns = [
    path("", views.superuser_admin_page, name="superuser_admin_page"),
    path("manage_post/<post_pk>", views.manage_post, name="manage_post"),
    path("add_post/", views.add_post, name="add_post"),
    path("delete_post/<post_pk>", views.delete_post, name="delete_post"),
    path(
        "superuser_view_product/<sku>",
        views.superuser_view_product,
        name='superuser_view_product'
    ),
    path(
        "superuser_view_order/<pk>",
        views.superuser_view_order,
        name="superuser_view_order"
    ),
    path("view_enquiry/<pk>", views.view_enquiry, name="view_enquiry")
]
