```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    user = request.user
    accounts = Account.objects.filter(user=user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']
            
            if transaction_type == 'deposit':
                accounts.first().balance += amount
                Transaction.objects.create(account=accounts.first(), amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
            elif transaction_type == 'withdraw':
                if accounts.first().balance >= amount:
                    accounts.first().balance -= amount
                    Transaction.objects.create(account=accounts.first(), amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient balance for withdrawal.')
            accounts.first().save()
            return redirect('manage_account')
    else:
        form = TransactionForm()

    context = {
        'accounts': accounts,
        'form': form,
    }
    return render(request, 'bank/manage_account.html', context)
```