```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@csrf_exempt
@require_http_methods(["GET", "POST"])
def account_management(request):
    if request.method == "GET":
        accounts = Account.objects.all()
        return render(request, 'account_management.html', {'accounts': accounts})

    if request.method == "POST":
        action = request.POST.get('action')
        account_id = request.POST.get('account_id')
        account = Account.objects.get(id=account_id)

        if action == "deposit":
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif action == "withdraw":
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'status': 'success', 'new_balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    return redirect('account_management')
```