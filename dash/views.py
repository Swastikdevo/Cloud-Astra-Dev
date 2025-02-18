```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
from django.core.exceptions import SuspiciousOperation

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = get_object_or_404(Account, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction_type = form.cleaned_data['transaction_type']
            amount = form.cleaned_data['amount']

            if transaction_type == 'deposit':
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')
            
            elif transaction_type == 'withdrawal':
                if amount > account.balance:
                    raise SuspiciousOperation("Insufficient funds for this withdrawal.")
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return redirect('manage_account')

    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/manage_account.html', {
        'account': account,
        'form': form,
        'transactions': transactions,
    })
```