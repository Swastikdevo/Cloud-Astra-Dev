```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        account_id = request.POST.get('account_id')
        action = request.POST.get('action')
        
        if action == 'create':
            account_name = request.POST.get('account_name')
            # Logic for account creation
            new_account = Account.objects.create(user=request.user, name=account_name)
            messages.success(request, f'Account {new_account.name} created successfully!')

        elif action == 'deposit':
            amount = float(request.POST.get('amount'))
            account = Account.objects.get(id=account_id, user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, f'Deposit of {amount} made to {account.name}.')

        elif action == 'withdraw':
            amount = float(request.POST.get('amount'))
            account = Account.objects.get(id=account_id, user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                messages.success(request, f'Withdrawal of {amount} made from {account.name}.')
            else:
                messages.error(request, 'Insufficient funds for this withdrawal.')

        return redirect('manage_account')

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'accounts': accounts})
```