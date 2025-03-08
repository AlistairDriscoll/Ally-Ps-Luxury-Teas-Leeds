from django.urls import path
from . import views

urlpatterns = [
    path("", views.superuser_admin_page, name="superuser_admin_page"),
    path("manage_post/<post_pk>", views.manage_post, name="manage_post"),
]
