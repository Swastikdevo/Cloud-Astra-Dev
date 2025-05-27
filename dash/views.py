```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful.'})
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'})
    
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-date')

    context = {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    }
    return render(request, 'bank/manage_account.html', context)
```