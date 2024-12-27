```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account
from .forms import DepositForm, WithdrawalForm

@csrf_exempt
def manage_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

    if request.method == 'GET':
        return render(request, 'account/detail.html', {'account': account})

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})
            return JsonResponse({'error': 'Invalid deposit amount'}, status=400)

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
                account.balance -= amount
                account.save()
                return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})
            return JsonResponse({'error': 'Invalid withdrawal amount'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
```