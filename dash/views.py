```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = BankAccount.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'message': 'Deposit successful!', 'balance': account.balance})

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = BankAccount.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'message': 'Withdrawal successful!', 'balance': account.balance})
                else:
                    return JsonResponse({'message': 'Insufficient funds'}, status=400)

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    account = BankAccount.objects.get(user=request.user)

    return render(request, 'manage_account.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'balance': account.balance,
    })
```