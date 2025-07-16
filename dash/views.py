```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_list')  # Redirect to account list view
    else:
        form = AccountForm()
    
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_list.html', {'accounts': accounts})

@login_required
def deposit(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount.isdigit() and float(amount) > 0:
            account.balance += float(amount)
            account.save()
            Transaction.objects.create(account=account, amount=float(amount), transaction_type='deposit')
            messages.success(request, f'Deposited ${amount} to your account!')
            return redirect('account_detail', account_id=account.id)
        else:
            messages.error(request, 'Please enter a valid amount.')
    
    return render(request, 'bank/deposit.html', {'account': account})

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})
```