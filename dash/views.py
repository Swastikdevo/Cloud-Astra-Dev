```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(owner=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']
            account_id = form.cleaned_data['account'].id
            
            account = Account.objects.get(id=account_id, owner=request.user)
            if transaction_type == 'deposit':
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            elif transaction_type == 'withdraw' and account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            else:
                return JsonResponse({'error': 'Insufficient funds for withdrawal.'}, status=400)

            return redirect('manage_account')
        return render(request, 'bank/manage_account.html', {'form': form, 'errors': form.errors})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
```