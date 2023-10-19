from django.contrib import admin
from .models import UserIncome, Source

class UserIncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'source', 'date')
    search_fields = ('description', 'source', 'date')

    # list_per_page = 10 #For pagination
# Register your models here.
admin.site.register(UserIncome, UserIncomeAdmin)
admin.site.register(Source)