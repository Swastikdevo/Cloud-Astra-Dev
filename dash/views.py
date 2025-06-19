```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date_created')[:10]
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            return handle_deposit(request, account)
        elif 'withdraw' in request.POST:
            return handle_withdraw(request, account)

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
    }
    
    return render(request, 'bank/account_overview.html', context)

@require_POST
def handle_deposit(request, account):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return redirect('account_overview')
    else:
        return JsonResponse({'errors': form.errors}, status=400)

@require_POST
def handle_withdraw(request, account):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount <= account.balance:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
            return redirect('account_overview')
        else:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)
    else:
        return JsonResponse({'errors': form.errors}, status=400)
```