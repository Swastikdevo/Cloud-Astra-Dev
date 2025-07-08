```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            # Update account balance
            account = Account.objects.get(user=request.user)
            if transaction.transaction_type == 'deposit':
                account.balance += transaction.amount
            elif transaction.transaction_type == 'withdraw':
                if account.balance >= transaction.amount:
                    account.balance -= transaction.amount
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
            account.save()
            return redirect('account_summary')
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    context = {
        'form': form,
        'transactions': transactions,
        'account_balance': Account.objects.get(user=request.user).balance,
    }
    return render(request, 'bank/manage_account.html', context)
```