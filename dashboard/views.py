from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from userincome.models import UserIncome
from expenses.models import Expense
from collections import defaultdict
from django.http import JsonResponse
import datetime
import json  

# Create your views here.
@login_required(login_url='/authentication/login')
def dashboard(request):

    def format_number(number):
        if number >= 1000:
            formatted_number = f'{number/1000:.1f}k'
        else:
            formatted_number = str(number)
        return formatted_number
    
    todays_date = datetime.date.today()
    start_date = todays_date - datetime.timedelta(days=30)
    expenses = Expense.objects.filter(
        owner=request.user,
        date__range=[start_date, todays_date]
    )
    incomes = UserIncome.objects.filter(
        owner=request.user,
        date__range=[start_date, todays_date]
    )
    
    expense_amt = 0
    for expense in expenses:
        expense_amt += expense.amount
    
    income_amt = 0
    for income in incomes:
        income_amt += income.amount

    expense_rate = expense_amt/30
    expense_rate = round(expense_rate, 2)

    income_rate = income_amt/30
    income_rate = round(income_rate, 2)

    expense_amount = format_number(expense_amt)
    income_amount = format_number(income_amt)

    context = {
        "income_amount": income_amount,
        "expense_amount": expense_amount,
        "expense_rate": expense_rate,
        "income_rate": income_rate,
        "recent_expenses" : expenses,
    }
    # print(context)
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='/authentication/login')
def get_charts_data(request):
    todays_date = datetime.date.today()
    start_date = datetime.date(todays_date.year, 1, 1)

    # Initialize dictionaries to hold monthly totals for expenses and income
    monthly_expenses = defaultdict(float)
    monthly_income = defaultdict(float)

    expenses = Expense.objects.filter(
        owner=request.user,
        date__range=[start_date, todays_date]
    )

    for expense in expenses:
        month = expense.date.strftime("%B")  # Get the month name
        monthly_expenses[month] += expense.amount

    incomes = UserIncome.objects.filter(
        owner=request.user,
        date__range=[start_date, todays_date]
    )

    for income in incomes:
        month = income.date.strftime("%B")  # Get the month name
        monthly_income[month] += income.amount

    # Prepare the data for the chart
    labels = list(monthly_expenses.keys())  # Month names
    data = {
        "expenses": list(monthly_expenses.values()),  # Expense totals
        "income": list(monthly_income.values()),  # Income totals
    }

    # Return the data as JSON
    chart_data = {
        "labels": labels,
        "data": data,
    }
    # print(chart_data)
    return JsonResponse({'monthly_data': chart_data}, safe=False)