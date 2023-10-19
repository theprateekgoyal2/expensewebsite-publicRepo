from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('get_charts_data/', views.get_charts_data, name='get_charts_data')
]