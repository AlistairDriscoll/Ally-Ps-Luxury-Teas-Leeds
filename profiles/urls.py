from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("view_order/<order_number>", views.view_order, name="view_order"),
    path("edit_profile/<userkey>", views.edit_profile, name="edit_profile"),
    path("edit_profile/account_deletion/<userkey>/",
         views.account_deletion, name="account_deletion"),
]
