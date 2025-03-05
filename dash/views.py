```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from .models import Account, Transaction

class BankManagementView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        action = request.GET.get('action')
        if action == 'get_balance':
            account_id = request.GET.get('account_id')
            return self.get_balance(account_id)
        elif action == 'get_transactions':
            account_id = request.GET.get('account_id')
            return self.get_transactions(account_id)
        return JsonResponse({'error': 'Invalid action'}, status=400)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'create_account':
            return self.create_account(request.POST)
        elif action == 'deposit':
            return self.deposit(request.POST)
        elif action == 'withdraw':
            return self.withdraw(request.POST)
        return JsonResponse({'error': 'Invalid action'}, status=400)

    def get_balance(self, account_id):
        try:
            account = Account.objects.get(id=account_id)
            return JsonResponse({'balance': account.balance})
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)

    def get_transactions(self, account_id):
        transactions = Transaction.objects.filter(account_id=account_id).values('amount', 'transaction_type', 'timestamp')
        return JsonResponse({'transactions': list(transactions)})

    def create_account(self, data):
        account = Account.objects.create(owner=data['owner'], balance=0)
        return JsonResponse({'message': 'Account created', 'account_id': account.id}, status=201)

    def deposit(self, data):
        account_id = data['account_id']
        amount = float(data['amount'])
        try:
            account = Account.objects.get(id=account_id)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)

    def withdraw(self, data):
        account_id = data['account_id']
        amount = float(data['amount'])
        try:
            account = Account.objects.get(id=account_id)
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