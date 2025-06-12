```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_account(request):
    user_accounts = Account.objects.filter(owner=request.user)

    if request.method == "POST":
        if "deposit" in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({"success": True, "message": "Deposit successful!"})
        
        elif "withdraw" in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({"success": True, "message": "Withdrawal successful!"})
                else:
                    return JsonResponse({"success": False, "message": "Insufficient funds!"})

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    
    context = {
        'user_accounts': user_accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    return render(request, 'manage_account.html', context)
```