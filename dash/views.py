```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']

            if transaction_type == 'deposit':
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                message = f'Deposit of {amount} completed successfully.'
            elif transaction_type == 'withdraw':
                if amount > account.balance:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                message = f'Withdrawal of {amount} completed successfully.'

            return JsonResponse({'message': message, 'new_balance': account.balance})

    return JsonResponse({'error': 'Invalid request'}, status=400)
```