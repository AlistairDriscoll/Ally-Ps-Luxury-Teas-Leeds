from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_blog_page, name="blog"),
    path("post/<pk>", views.blog_post, name="blog_post"),
]
