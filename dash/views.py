```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        account = Account.objects.get(user=request.user)

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'message': 'Deposit successful!', 'balance': account.balance})
            else:
                return JsonResponse({'error': form.errors}, status=400)

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'message': 'Withdrawal successful!', 'balance': account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)
            else:
                return JsonResponse({'error': form.errors}, status=400)

    # Render the account management page
    context = {
        'account': Account.objects.get(user=request.user)
    }
    return render(request, 'manage_account.html', context)
```