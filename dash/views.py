```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
from decimal import Decimal

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(user=request.user)
            transaction_type = form.cleaned_data['transaction_type']
            amount = form.cleaned_data['amount']
            
            if transaction_type == 'deposit':
                account.balance += Decimal(amount)
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            elif transaction_type == 'withdrawal':
                if account.balance >= Decimal(amount):
                    account.balance -= Decimal(amount)
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
            account.save()
            return JsonResponse({'success': True, 'new_balance': str(account.balance)})
    else:
        form = TransactionForm()
    
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')
    return render(request, 'manage_account.html', {'form': form, 'transactions': transactions})
```