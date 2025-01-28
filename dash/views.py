```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def account_view(request):
    account = Account.objects.get(user=request.user)  # Get the logged-in user's account

    if request.method == "POST":
        # Handle deposit
        deposit_form = DepositForm(request.POST)
        withdrawal_form = WithdrawalForm(request.POST)

        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})

        if withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})
            else:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
    
    transactions = Transaction.objects.filter(account=account).order_by('-date')  # Fetch account transactions

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions
    }
    
    return render(request, 'bank/account.html', context)
```