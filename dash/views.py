```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, AccountCreationForm

@login_required
def bank_management_view(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountCreationForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('bank_management')
        
        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful'})
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful'})
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank_management.html', {'accounts': accounts})
```