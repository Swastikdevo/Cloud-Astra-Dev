```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
from django.utils import timezone

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = request.user.account  # assuming a one-to-one relation
            transaction.timestamp = timezone.now()
            transaction.save()
            
            # Optionally, update account balance
            if transaction.transaction_type == 'Deposit':
                request.user.account.balance += transaction.amount
            elif transaction.transaction_type == 'Withdrawal':
                if request.user.account.balance >= transaction.amount:
                    request.user.account.balance -= transaction.amount
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
            request.user.account.save()

            return JsonResponse({'success': 'Transaction successful', 'balance': request.user.account.balance}, status=200)
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=request.user.account).order_by('-timestamp')
    
    return render(request, 'manage_account.html', {'form': form, 'transactions': transactions})
```