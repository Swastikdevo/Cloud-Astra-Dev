```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.decorators import method_decorator

@login_required
@csrf_exempt
def bank_account_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/accounts.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_account':
            account_name = request.POST.get('account_name')
            initial_balance = float(request.POST.get('initial_balance'))
            Account.objects.create(user=request.user, name=account_name, balance=initial_balance)
            messages.success(request, 'Account created successfully.')
            return redirect('bank_account_view')

        elif action == 'deposit':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount'))
            account = get_object_or_404(Account, id=account_id, user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, 'Deposit successful.')
            return redirect('bank_account_view')

        elif action == 'withdraw':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount'))
            account = get_object_or_404(Account, id=account_id, user=request.user)

            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                messages.success(request, 'Withdrawal successful.')
            else:
                messages.error(request, 'Insufficient balance.')
            return redirect('bank_account_view')

        elif action == 'view_transactions':
            account_id = request.POST.get('account_id')
            transactions = Transaction.objects.filter(account__id=account_id)
            transaction_data = [{'date': txn.date, 'amount': txn.amount, 'type': txn.transaction_type} for txn in transactions]
            return JsonResponse({'transactions': transaction_data})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)
```