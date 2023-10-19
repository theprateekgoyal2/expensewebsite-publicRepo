from django.shortcuts import render
import os, json
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import UserPrefernce
from django.contrib.auth.models import User
from expenses.models import Category
from expenses import urls, views
from userincome.models import Source
from django.contrib import messages

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            currency_data.append({'name': key, 'value': value})
    exists = UserPrefernce.objects.filter(user=request.user).exists()
    user_prefernces = None
    if exists: 
        user_prefernces = UserPrefernce.objects.get(user=request.user)
    if request.method=='GET':
        return render(request, 'userprefernces/index.html', {'currencies': currency_data, 'user_prefernces': user_prefernces})
    else:
        currency = request.POST['currency']
        if exists:
            user_prefernces.currency=currency
            user_prefernces.save()
        else:
            UserPrefernce.objects.create(user=request.user, currency=currency)
        messages.success(request, "Changes are saved")
        return render(request, 'userprefernces/index.html', {'currencies': currency_data, 'user_prefernces': user_prefernces})
    
@login_required(login_url='/authentication/login')
def account_details(request):
    context = {
        'user': request.user,
        'categories': Category.objects.all(), 
        'sources': Source.objects.all()
    }
    if request.method == "GET":
        return render (request, 'userprefernces/account-details.html', context)
    
    # print(context)
    return render (request, 'userprefernces/account-details.html', context)
