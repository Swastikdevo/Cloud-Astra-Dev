```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank_management.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_account':
            account_name = request.POST.get('account_name')
            account_balance = request.POST.get('initial_balance', 0)
            account = Account.objects.create(
                user=request.user,
                name=account_name,
                balance=account_balance
            )
            messages.success(request, f'Account "{account.name}" created successfully!')
            return redirect('bank_management')

        elif action == 'deposit':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount', 0))
            try:
                account = Account.objects.get(id=account_id, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, f'Deposited ${amount} to "{account.name}".')
            except ObjectDoesNotExist:
                messages.error(request, 'Account not found.')
            return redirect('bank_management')

        elif action == 'withdraw':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount', 0))
            try:
                account = Account.objects.get(id=account_id, user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    messages.success(request, f'Withdrew ${amount} from "{account.name}".')
                else:
                    messages.error(request, 'Insufficient funds.')
            except ObjectDoesNotExist:
                messages.error(request, 'Account not found.')
            return redirect('bank_management')

        elif action == 'view_transactions':
            account_id = request.POST.get('account_id')
            transactions = Transaction.objects.filter(account_id=account_id)
            return JsonResponse({'transactions': list(transactions.values())})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
```