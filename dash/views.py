```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deposit':
            return handle_deposit(request)
        elif action == 'withdraw':
            return handle_withdrawal(request)
        elif action == 'transaction_history':
            return get_transaction_history(request)
    
    return render(request, 'account/manage_account.html')

def handle_deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, type='deposit')
        return JsonResponse({'status': 'success', 'balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

def handle_withdrawal(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, type='withdrawal')
            return JsonResponse({'status': 'success', 'balance': account.balance})
        return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'errors': form.errors})

def get_transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    transaction_list = [{'date': tx.date, 'amount': tx.amount, 'type': tx.type} for tx in transactions]
    return JsonResponse({'status': 'success', 'transactions': transaction_list})
```