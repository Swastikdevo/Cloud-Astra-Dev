```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import BankAccount, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                bank_account = BankAccount.objects.get(user=request.user)
                bank_account.balance += amount
                bank_account.save()
                Transaction.objects.create(account=bank_account, amount=amount, transaction_type='deposit')
                return JsonResponse({'message': 'Deposit successful', 'balance': bank_account.balance})

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                bank_account = BankAccount.objects.get(user=request.user)
                if bank_account.balance >= amount:
                    bank_account.balance -= amount
                    bank_account.save()
                    Transaction.objects.create(account=bank_account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'message': 'Withdrawal successful', 'balance': bank_account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        bank_account = BankAccount.objects.get(user=request.user)
    
    return render(request, 'account/manage_account.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'balance': bank_account.balance,
    })
```