```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@csrf_exempt
def bank_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/bank_dashboard.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        account_id = request.POST.get('account_id')

        try:
            account = Account.objects.get(id=account_id, user=request.user)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found.'}, status=404)

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': 'Deposit successful.', 'new_balance': account.balance})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return JsonResponse({'success': 'Withdrawal successful.', 'new_balance': account.balance})

        return JsonResponse({'error': 'Invalid action or form data.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
```