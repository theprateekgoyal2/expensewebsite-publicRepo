from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="prefernces"),
    path("account-details", views.account_details, name="account-details")
]
