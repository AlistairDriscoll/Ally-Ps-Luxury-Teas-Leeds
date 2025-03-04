from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_blog_page, name="blog"),
]
