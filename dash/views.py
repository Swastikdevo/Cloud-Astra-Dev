```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(user=request.user)

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                account.balance += amount
                account.save()
                return redirect('account_dashboard')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    account.balance -= amount
                    account.save()
                    return redirect('account_dashboard')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    context = {
        'accounts': user_accounts,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'account_dashboard.html', context)
```