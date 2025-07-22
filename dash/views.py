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
        transactions = Transaction.objects.filter(account__in=accounts)
        return render(request, 'bank/manage_account.html', {
            'accounts': accounts,
            'transactions': transactions,
            'transaction_form': TransactionForm()
        })
    
    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']

            if transaction_type == 'deposit':
                account.balance += amount
                action = 'Deposited'
            elif transaction_type == 'withdraw' and account.balance >= amount:
                account.balance -= amount
                action = 'Withdrew'
            else:
                return JsonResponse({'error': 'Insufficient funds or invalid transaction type.'}, status=400)

            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)
            return JsonResponse({'message': f'Successfully {action} ${amount}.'}, status=200)

        return JsonResponse({'error': 'Invalid form submission.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
```