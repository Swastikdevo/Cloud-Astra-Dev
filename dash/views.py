```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'balance': account.balance})
            return JsonResponse({'status': 'error', 'errors': form.errors})

        elif request.POST.get('action') == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'status': 'success', 'balance': account.balance})
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
            return JsonResponse({'status': 'error', 'errors': form.errors})

    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')
    return render(request, 'manage_account.html', {'account': account, 'transactions': transactions})
```