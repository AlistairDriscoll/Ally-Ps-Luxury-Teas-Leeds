from django.urls import path
from . import views

urlpatterns = [
    path("", views.superuser_admin_page, name="superuser_admin_page"),
]
