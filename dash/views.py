```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        account = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(account=account).order_by('-date')
        return render(request, 'account_management.html', {'account': account, 'transactions': transactions})

    elif request.method == 'POST':
        action_type = request.POST.get('action')

        if action_type == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'message': 'Deposit successful.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid deposit amount.'})

        elif action_type == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)

                if amount > account.balance:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds.'})

                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return JsonResponse({'success': True, 'message': 'Withdrawal successful.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid withdrawal amount.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
```