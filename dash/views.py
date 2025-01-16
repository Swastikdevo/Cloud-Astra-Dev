```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                # Perform deposit operation
                account.deposit(amount)
                return JsonResponse({'status': 'success', 'message': 'Deposit successful'})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                # Perform withdrawal operation
                if account.withdraw(amount):
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                source_account = form.cleaned_data['source_account']
                target_account = form.cleaned_data['target_account']
                amount = form.cleaned_data['amount']
                # Perform transfer operation
                if source_account.transfer(target_account, amount):
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Transfer failed'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
```