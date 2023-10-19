from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="income"),
    path('add-income', views.add_income, name="add-income"),
    path('edit_income/<int:id>', views.edit_income, name="edit_income"),
    path('income-delete/<int:id>', views.delete_income, name="income-delete"),
    path('search-income', csrf_exempt(views.search_income), name="search-income"),
    path('income_source_summary/<str:time_interval>/', views.income_source_summary, name="income_source_summary"),
    path('income-stats', views.stats_view, name="income-stats"),
]