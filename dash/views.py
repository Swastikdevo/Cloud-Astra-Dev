```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

@method_decorator(login_required, name='dispatch')
class BankAccountView(View):

    def get(self, request):
        accounts = BankAccount.objects.filter(user=request.user)
        return render(request, 'bank/accounts.html', {'accounts': accounts})

    @csrf_exempt
    def post(self, request):
        action = request.POST.get('action')

        if action == 'create':
            account_type = request.POST.get('account_type')
            initial_balance = request.POST.get('initial_balance', 0)
            account = BankAccount.objects.create(
                user=request.user,
                account_type=account_type,
                balance=initial_balance
            )
            return JsonResponse({'status': 'success', 'account_id': account.id})

        elif action == 'deposit':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount', 0))

            try:
                account = BankAccount.objects.get(id=account_id, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Account not found'})

        elif action == 'withdraw':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount', 0))

            try:
                account = BankAccount.objects.get(id=account_id, user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
                    return JsonResponse({'status': 'success', 'new_balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Account not found'})

        return JsonResponse({'status': 'error', 'message': 'Invalid action'})
```