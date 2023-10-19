from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expense', views.add_expense, name="add-expense"),
    # path('add-category', views.add_category, name="add-category"),
    path('edit_expense/<int:id>', views.edit_expense, name="edit_expense"),
    path('expense-delete/<int:id>', views.delete_expense, name="expense-delete"),
    path('search-expenses', csrf_exempt(views.search_expenses), name="search-expenses"),
    path('expense_category_summary/<str:time_interval>/', views.expense_category_summary, name="expense_category_summary"),
    path('stats', views.stats_view, name="stats"),
    path('export-csv', views.export_csv, name="export-csv"),
    path('export-excel', views.export_excel, name="export-excel"),
    path('upload_expense_csv', views.upload_expense_csv, name='upload_expense_csv'),
]