```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@csrf_exempt
@login_required
def manage_account(request):
    """
    View to manage bank account operations: view balance, make deposits/withdrawals.
    This view features enhanced transaction history and account summaries.
    """
    if request.method == 'GET':
        account = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(account=account).order_by('-date')
        total_balance = account.balance

        return render(request, 'account/manage_account.html', {
            'account': account,
            'transactions': transactions,
            'total_balance': total_balance,
            'form': TransactionForm()
        })

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(user=request.user)

            if transaction.transaction_type == 'deposit':
                transaction.account.balance += transaction.amount
            elif transaction.transaction_type == 'withdraw' and transaction.amount <= transaction.account.balance:
                transaction.account.balance -= transaction.amount
            else:
                return JsonResponse({'error': 'Insufficient funds for withdrawal'}, status=400)

            transaction.save()
            transaction.account.save()

            return JsonResponse({'message': 'Transaction successful', 'new_balance': transaction.account.balance})

        return JsonResponse({'error': 'Invalid form submission'}, status=400)
```