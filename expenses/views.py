from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
import json, csv, xlwt
from django.http import JsonResponse, HttpResponse
from userprefernces.models import UserPrefernce
from userprefernces.views import account_details
import datetime
from django.template.loader import render_to_string
from .forms import ExpenseUploadForm
from django.views.decorators.csrf import csrf_exempt
# import tempfile
# from weasyprint import HTML
# from django.db.models import Sum

# Create your views here.
def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(date__istartswith=search_str, owner=request.user) | Expense.objects.filter(description__icontains=search_str, owner=request.user) | Expense.objects.filter(category__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # Check if UserPreference exists for the current user
    try:
        user_preference = UserPrefernce.objects.get(user=request.user)
        currency = user_preference.currency
    except UserPrefernce.DoesNotExist:
        # Handle the case where UserPreference doesn't exist (new user)
        currency = None

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    # Check if the user has set their preferences
    try:
        user_preference = UserPrefernce.objects.get(user=request.user)
    except UserPrefernce.DoesNotExist:
        messages.error(request, "Please set your preferences before adding an expense.")
        return redirect('prefernces')
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount required.')
            return render(request, 'expenses/add_expense.html', context)
    
        if not description:
            messages.error(request, 'Description required.')
            return render(request, 'expenses/add_expense.html', context)
        
        Expense.objects.create(owner = request.user, amount=amount, description=description, date=date, category=category)
        messages.success(request, "Expense saved successfully")
        return redirect('expenses') 

@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount required.')
            return render(request, 'expenses/edit_expense.html', context)
        
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
    
        if not description:
            messages.error(request, 'description is required.')
            return render(request, 'expenses/edit_expense.html', context)
        
        expense.owner = request.user
        expense.amount=amount
        expense.description=description
        expense.date=date
        expense.category=category
        expense.save()
        messages.success(request, "Expense updated successfully")
        return redirect('expenses') 

@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense deleted.")
    return redirect('expenses')

# def add_category(request):
#     print('view connected')
#     if request.method == 'POST':
#         category = request.POST["category"]
#     Category.objects.create(name = category)
#     messages.success(request, "Category added successfully")
#     return redirect(request, 'account-details')
@login_required(login_url='/authentication/login')
def expense_category_summary(request, time_interval):
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
    # # Filter expenses based on the start_date
    expenses = Expense.objects.filter(
        owner=request.user,
        date__range=[start_date, todays_date]
    )
    finalrep = {}
    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount
    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)
@login_required(login_url='/authentication/login')
def stats_view(request):
    return render (request, 'expenses/stats.html')
@login_required(login_url='/authentication/login')
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    username = request.user.username
    response['Content-Disposition']='attachment; filename=Expenses-For-'+ username +'-'+ datetime.datetime.now().strftime("%Y-%m-%d")+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    
    return response
@login_required(login_url='/authentication/login')
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    username = request.user.username
    response['Content-Disposition']='attachment; filename=Expenses-For-'+ username +'-'+ datetime.datetime.now().strftime("%Y-%m-%d")+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list(
        'amount', 'description', 'category', 'date')
    
    for row in rows: 
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    
    wb.save(response)
    return response

def upload_expense_csv(request):
    if request.method == 'POST':
        form = ExpenseUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']

            if csv_file:
                # Process the uploaded CSV file
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())

                for row in csv_data:
                    # Assuming your CSV structure is: amount, date, description, category
                    amount, date, description, category = row
                    # Create an Expense record
                    Expense.objects.create(
                        owner=request.user,
                        amount=amount,
                        date=date,
                        description=description,
                        category=category
                    )

                return redirect('expenses')

    else:
        form = ExpenseUploadForm()

    return render(request, 'upload_expense.html', {'form': form})

# def export_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     username = request.user.username
#     response['Content-Disposition']='attachment; filename=Expenses-For-'+ username +'-'+ datetime.datetime.now().strftime("%Y-%m-%d")+'.pdf'
#     response['Content-Transfer-Encoding']= 'binary'

#     html_string = render_to_string('expenses/pdf-output.html', {'expenses':[],'total':0})
#     html = HTML(string=html_string)

#     result = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()

#         output = open(output.name, 'rb')
#         response.write(output.read())

#     return response  
