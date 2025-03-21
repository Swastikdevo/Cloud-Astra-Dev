```python
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action', None)
        account_id = request.POST.get('account_id', None)

        try:
            account = Account.objects.get(id=account_id, user=request.user)

            if action == 'deposit':
                amount = float(request.POST.get('amount', 0))
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful', 'new_balance': account.balance})

            elif action == 'withdraw':
                amount = float(request.POST.get('amount', 0))
                if amount > account.balance:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                return JsonResponse({'status': 'success', 'message': 'Withdrawal successful', 'new_balance': account.balance})

            elif action == 'transfer':
                target_account_id = request.POST.get('target_account_id', None)
                target_account = Account.objects.get(id=target_account_id)
                amount = float(request.POST.get('amount', 0))

                if amount > account.balance:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

                account.balance -= amount
                target_account.balance += amount
                account.save()
                target_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='transfer_to', target_account=target_account)
                Transaction.objects.create(account=target_account, amount=amount, transaction_type='transfer_from', source_account=account)
                return JsonResponse({'status': 'success', 'message': 'Transfer successful', 'new_balance': account.balance})

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found'})

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'accounts': accounts})
```