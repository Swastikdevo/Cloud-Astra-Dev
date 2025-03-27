```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def account_dashboard(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_dashboard')
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('account_dashboard')
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()

    context = {
        'accounts': accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    
    return render(request, 'bank/account_dashboard.html', context)
```