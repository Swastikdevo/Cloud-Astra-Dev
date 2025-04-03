```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    account = get_object_or_404(Account, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        withdrawal_form = WithdrawalForm(request.POST)
        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return redirect('account_overview')
        elif withdrawal_form.is_valid() and account.balance >= withdrawal_form.cleaned_data['amount']:
            amount = withdrawal_form.cleaned_data['amount']
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return redirect('account_overview')
    
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
  
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    
    return render(request, 'bank/account_overview.html', context)

@require_POST
@login_required
def ajax_transaction_history(request):
    account = get_object_or_404(Account, owner=request.user)
    transactions = Transaction.objects.filter(account=account).values('date', 'amount', 'transaction_type')
    
    return JsonResponse(list(transactions), safe=False)
```