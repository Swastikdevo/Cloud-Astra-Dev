```python
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

class BankAccountView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.accounts = {}  # A simple in-memory storage for demo purposes

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create_account':
            account_id = len(self.accounts) + 1
            self.accounts[account_id] = {
                'balance': 0.0,
                'owner': data.get('owner')
            }
            return JsonResponse({'status': 'success', 'account_id': account_id}, status=201)

        elif action == 'deposit':
            account_id = data.get('account_id')
            amount = data.get('amount', 0)
            if account_id in self.accounts:
                self.accounts[account_id]['balance'] += amount
                return JsonResponse({'status': 'success', 'balance': self.accounts[account_id]['balance']})
            else:
                return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)

        elif action == 'withdraw':
            account_id = data.get('account_id')
            amount = data.get('amount', 0)
            if account_id in self.accounts:
                if self.accounts[account_id]['balance'] >= amount:
                    self.accounts[account_id]['balance'] -= amount
                    return JsonResponse({'status': 'success', 'balance': self.accounts[account_id]['balance']})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

    def get(self, request):
        account_id = request.GET.get('account_id')
        if account_id and account_id.isdigit():
            account_id = int(account_id)
            if account_id in self.accounts:
                return JsonResponse({'status': 'success', 'account': self.accounts[account_id]})
            else:
                return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)

        return JsonResponse({'status': 'error', 'message': 'No account ID provided'}, status=400)
```