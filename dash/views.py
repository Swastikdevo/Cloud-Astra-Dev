```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def manage_account(request):
    """View to handle account management including deposit, withdrawal, and transaction history."""
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful!', 'new_balance': user_account.balance})
        
        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!', 'new_balance': user_account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})

    transactions = Transaction.objects.filter(account=user_account).order_by('-created_at')
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()

    context = {
        'account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    return render(request, 'bank/manage_account.html', context)
```