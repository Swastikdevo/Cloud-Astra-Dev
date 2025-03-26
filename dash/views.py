```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction  # Assuming you have these models defined

@login_required
@csrf_exempt
def account_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account/account_overview.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_account':
            account_name = request.POST.get('account_name')
            balance = request.POST.get('balance', 0)

            new_account = Account.objects.create(user=request.user, name=account_name, balance=balance)
            messages.success(request, f'Account {new_account.name} created successfully!')

        elif action == 'deposit':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount', 0))

            account = Account.objects.get(id=account_id, user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, f'Deposited {amount} to {account.name} successfully!')

        elif action == 'withdraw':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount', 0))

            account = Account.objects.get(id=account_id, user=request.user)
            if amount > account.balance:
                messages.error(request, 'Insufficient funds for withdrawal.')
            else:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                messages.success(request, f'Withdrew {amount} from {account.name} successfully!')

        return redirect('account_view')

    return JsonResponse({'error': 'Invalid request method'}, status=400)
```