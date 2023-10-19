from django.shortcuts import render, redirect
from .models import UserIncome, Source
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
import datetime
from userprefernces.models import UserPrefernce

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPrefernce.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount required.')
            return render(request, 'income/add_income.html', context)
    
        if not description:
            messages.error(request, 'Description required.')
            return render(request, 'income/add_income.html', context)
        
        UserIncome.objects.create(owner = request.user, amount=amount, description=description, date=date, source=source)
        messages.success(request, "Record saved successfully")
        return redirect('income')

@login_required(login_url='/authentication/login')
def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount required.')
            return render(request, 'income/edit_income.html', context)
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
    
        if not description:
            messages.error(request, 'description is required.')
            return render(request, 'income/edit_income.html', context)
        
        income.amount=amount
        income.description=description
        income.date=date
        income.source=source
        income.save()
        messages.success(request, "Record updated successfully")
        return redirect('income') 

@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Record deleted.")
    return redirect('income') 

@login_required(login_url='/authentication/login')
def income_source_summary(request, time_interval):
    # Convert the time_interval to the number of days (e.g., '1m' for 1 month)
    if time_interval == '1m':
        num_days = 30
    elif time_interval == '3m':
        num_days = 90
    elif time_interval == '6m':
        num_days = 180
    elif time_interval == '1y':
        num_days = 365
    else:
        # Handle an invalid time_interval here
        num_days = 0
    # print(num_days,"--time interval")
    todays_date = datetime.date.today()
    start_date = todays_date - datetime.timedelta(days=num_days)
    # print(datetime.timedelta(days=num_days))
    # print(todays_date, start_date, "-----time period")
    # # Filter incomes based on the start_date
    incomes = UserIncome.objects.filter(
        owner=request.user,
        date__range=[start_date, todays_date]
    )
    finalrep = {}
    def get_category(income):
        return income.source
    source_list = list(set(map(get_category, incomes)))
    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount
    for x in incomes:
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)

    return JsonResponse({'income_source_data': finalrep}, safe=False)

@login_required(login_url='/authentication/login')
def stats_view(request):
    return render (request, 'income/income-stats.html')