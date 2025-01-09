```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            account_name = request.POST.get('account_name')
            new_account = Account(user=request.user, name=account_name)
            new_account.save()
            messages.success(request, 'Account created successfully!')
        
        elif action == 'delete':
            account_id = request.POST.get('account_id')
            try:
                account = Account.objects.get(id=account_id, user=request.user)
                account.delete()
                messages.success(request, 'Account deleted successfully!')
            except Account.DoesNotExist:
                messages.error(request, 'Account not found!')

        elif action == 'transfer':
            account_id = request.POST.get('account_id')
            target_account_id = request.POST.get('target_account_id')
            amount = float(request.POST.get('amount'))
            try:
                source_account = Account.objects.get(id=account_id, user=request.user)
                target_account = Account.objects.get(id=target_account_id, user=request.user)

                if source_account.balance >= amount:
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()

                    Transaction.objects.create(source_account=source_account, target_account=target_account, amount=amount)
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
            except Account.DoesNotExist:
                messages.error(request, 'One of the accounts does not exist!')

        return redirect('manage_account')

    return JsonResponse({'status': 'invalid method'}, status=400)
```