```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
from django.utils.decorators import method_decorator

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')[:10]
    
    context = {
        'accounts': accounts,
        'transactions': transactions,
    }
    return render(request, 'bank/dashboard.html', context)

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = get_object_or_404(Account, id=request.POST['account_id'], user=request.user)
            transaction.save()
            return redirect('bank:dashboard')
    else:
        form = TransactionForm()
    
    return render(request, 'bank/create_transaction.html', {'form': form})

@login_required
def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/account_details.html', context)

@login_required
def deposit(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount.isdigit() and int(amount) > 0:
            account.balance += int(amount)
            account.save()
            Transaction.objects.create(account=account, amount=int(amount), transaction_type='deposit')
            return JsonResponse({'success': True, 'new_balance': account.balance})
    return JsonResponse({'success': False, 'error': 'Invalid amount'}, status=400)

@login_required
def withdraw(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount.isdigit() and int(amount) > 0 and int(amount) <= account.balance:
            account.balance -= int(amount)
            account.save()
            Transaction.objects.create(account=account, amount=int(amount), transaction_type='withdrawal')
            return JsonResponse({'success': True, 'new_balance': account.balance})
    return JsonResponse({'success': False, 'error': 'Invalid amount or insufficient funds'}, status=400)
```