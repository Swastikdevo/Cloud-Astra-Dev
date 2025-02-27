```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.core.exceptions import PermissionDenied

@login_required
def manage_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, type='deposit')
                return redirect('account_detail', account_id=account.id)
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, type='withdraw')
                    return redirect('account_detail', account_id=account.id)
                else:
                    form.add_error('amount', 'Insufficient funds')
        else:
            raise PermissionDenied()
    else:
        form = DepositForm()
        withdraw_form = WithdrawForm()
    
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    return render(request, 'account/manage_account.html', {
        'account': account,
        'form': form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    })
```