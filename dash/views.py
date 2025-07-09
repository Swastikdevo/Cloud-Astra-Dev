```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required

class BankView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    @require_POST
    def create_account(self, request):
        data = json.loads(request.body)
        account = Account.objects.create(
            user=request.user,
            account_number=data['account_number'],
            balance=data['initial_balance']
        )
        return JsonResponse({'message': 'Account created successfully', 'account_id': account.id})

    @method_decorator(login_required)
    @require_GET
    def get_account(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id, user=request.user)
            return JsonResponse({
                'account_number': account.account_number,
                'balance': account.balance
            })
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    @require_POST
    def deposit(self, request):
        data = json.loads(request.body)
        try:
            account = Account.objects.get(id=data['account_id'], user=request.user)
            amount = data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    @require_POST
    def withdraw(self, request):
        data = json.loads(request.body)
        try:
            account = Account.objects.get(id=data['account_id'], user=request.user)
            amount = data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})
            else:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)
```