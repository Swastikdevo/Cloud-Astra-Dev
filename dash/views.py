```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

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
                transaction = Transaction(account=user_account, amount=amount, transaction_type='Deposit')
                transaction.save()
                return JsonResponse({'success': True, 'new_balance': user_account.balance})
        
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > user_account.balance:
                    return JsonResponse({'success': False, 'message': 'Insufficient balance'})
                user_account.balance -= amount
                user_account.save()
                transaction = Transaction(account=user_account, amount=amount, transaction_type='Withdraw')
                transaction.save()
                return JsonResponse({'success': True, 'new_balance': user_account.balance})

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-timestamp')[:10]

    context = {
        'user_account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions
    }
    return render(request, 'manage_account.html', context)
```