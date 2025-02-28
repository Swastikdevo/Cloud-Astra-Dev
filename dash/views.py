```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
import json

class BankManagementView(View):
    
    @method_decorator(csrf_exempt)
    @require_POST
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create_account':
            return self.create_account(data)
        elif action == 'deposit':
            return self.deposit(data)
        elif action == 'withdraw':
            return self.withdraw(data)
        elif action == 'check_balance':
            return self.check_balance(data)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    def create_account(self, data):
        account_name = data.get('account_name')
        initial_balance = data.get('initial_balance', 0)

        # Logic to create an account in the database would go here
        # For now, we return a placeholder response
        return JsonResponse({'message': 'Account created', 'account_name': account_name, 'balance': initial_balance}, status=201)

    def deposit(self, data):
        account_id = data.get('account_id')
        amount = data.get('amount', 0)

        # Logic to deposit the amount into the account would go here
        # For now, we return a placeholder response
        return JsonResponse({'message': 'Deposit successful', 'account_id': account_id, 'amount': amount}, status=200)

    def withdraw(self, data):
        account_id = data.get('account_id')
        amount = data.get('amount', 0)

        # Logic to withdraw the amount from the account would go here
        # For now, we return a placeholder response
        return JsonResponse({'message': 'Withdrawal successful', 'account_id': account_id, 'amount': amount}, status=200)

    def check_balance(self, data):
        account_id = data.get('account_id')

        # Logic to check the balance would go here
        # For now, we return a placeholder response
        return JsonResponse({'message': 'Balance checked', 'account_id': account_id, 'balance': 1000}, status=200)
```