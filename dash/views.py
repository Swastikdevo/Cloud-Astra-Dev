```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Account, Transaction
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required, name='dispatch')
class BankView(View):

    @require_http_methods(["POST"])
    def deposit(self, request):
        account_id = request.POST.get('account_id')
        amount = float(request.POST.get('amount'))
        account = get_object_or_404(Account, id=account_id)
        account.balance += amount
        account.save()
        transaction = Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})

    @require_http_methods(["POST"])
    def withdraw(self, request):
        account_id = request.POST.get('account_id')
        amount = float(request.POST.get('amount'))
        account = get_object_or_404(Account, id=account_id)
        if amount > account.balance:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)
        account.balance -= amount
        account.save()
        transaction = Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
        return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})

    @require_http_methods(["GET"])
    def get_balance(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        return JsonResponse({'account_id': account.id, 'balance': account.balance})

    @require_http_methods(["GET"])
    def transaction_history(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        transactions = account.transaction_set.all().values('id', 'amount', 'transaction_type', 'created_at')
        return JsonResponse({'account_id': account.id, 'transactions': list(transactions)})
```