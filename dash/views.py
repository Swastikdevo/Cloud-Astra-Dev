```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = Account.objects.get(user=request.user)

    # Handle deposit
    if request.method == "POST" and "deposit" in request.POST:
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return redirect('manage_account')
    else:
        deposit_form = DepositForm()

    # Handle withdrawal
    if request.method == "POST" and "withdraw" in request.POST:
        withdrawal_form = WithdrawalForm(request.POST)
        if withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return redirect('manage_account')
            else:
                return JsonResponse({'error': 'Insufficient funds.'}, status=400)
    else:
        withdrawal_form = WithdrawalForm()

    # Fetch recent transactions
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')[:10]

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    }

    return render(request, 'bank/manage_account.html', context)
```