from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Transaction, Category, RecurringPayment
from .forms import TransactionForm,LoginForm,AuthenticationForm
from datetime import date
from django.contrib.auth import login, authenticate

def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)

    total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expenses

 
    expenses_by_category = (
        transactions.filter(transaction_type='expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    print("Expenses by Category:", expenses_by_category)


    monthly_summary = (
        transactions
        .annotate(month=TruncMonth('date'))
        .values('month', 'transaction_type')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    print("Monthly Summary:", monthly_summary)
    
    upcoming_payments = RecurringPayment.objects.filter(user=request.user, due_date__gte=date.today())

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
        'transactions': transactions,
        'expenses_by_category': list(expenses_by_category), 
        'monthly_summary': monthly_summary,
        'upcoming_payments': upcoming_payments,
    }

    return render(request, 'finance/dashboard.html', context)
from django.shortcuts import render, redirect
from .forms import TransactionForm

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')  
    else:
        form = TransactionForm()
    return render(request, 'finance/add_transaction.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  
    else:
        form = LoginForm()
    return render(request, 'finance/login.html', {'form': form})
