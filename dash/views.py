```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
from django.core.exceptions import ObjectDoesNotExist

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction_type = form.cleaned_data['transaction_type']
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)

            if transaction_type == 'deposit':
                account.balance += amount
                Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)
            elif transaction_type == 'withdraw':
                if account.balance >= amount:
                    account.balance -= amount
                    Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

            account.save()
            return JsonResponse({'success': True, 'balance': account.balance})

    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    return render(request, 'manage_account.html', {'form': form, 'transactions': transactions})
```