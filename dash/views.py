```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/accounts.html', {'accounts': accounts})

    @csrf_exempt
    def post(self, request):
        action = request.POST.get('action')
        if action == 'create_account':
            account_name = request.POST.get('account_name')
            account_balance = request.POST.get('initial_balance', 0)
            new_account = Account.objects.create(
                user=request.user,
                name=account_name,
                balance=account_balance
            )
            return JsonResponse({'status': 'success', 'account_id': new_account.id})

        elif action == 'deposit':
            account_id = request.POST.get('account_id')
            amount = request.POST.get('amount', 0)
            account = Account.objects.get(id=account_id, user=request.user)
            account.balance += float(amount)
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif action == 'withdraw':
            account_id = request.POST.get('account_id')
            amount = request.POST.get('amount', 0)
            account = Account.objects.get(id=account_id, user=request.user)
            if account.balance >= float(amount):
                account.balance -= float(amount)
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

        return JsonResponse({'status': 'error', 'message': 'Invalid action'})
```