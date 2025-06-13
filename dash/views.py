```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views import View
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@method_decorator(require_POST, name='dispatch')
class BankManagementView(View):
    def get(self, request):
        accounts = Account.objects.all()
        account_form = AccountForm()
        transaction_form = TransactionForm()
        return render(request, 'bank_management/home.html', {
            'accounts': accounts,
            'account_form': account_form,
            'transaction_form': transaction_form,
        })

    def post(self, request):
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                account_form.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
            return JsonResponse({'status': 'error', 'message': 'Account creation failed!'})

        elif 'create_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction_form.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully!'})
            return JsonResponse({'status': 'error', 'message': 'Transaction failed!'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request!'})

    def update_account_balance(self, account_id, amount):
        try:
            account = Account.objects.get(pk=account_id)
            account.balance += amount
            account.save()
            return True
        except Account.DoesNotExist:
            return False

    def get_transaction_history(self, account_id):
        transactions = Transaction.objects.filter(account_id=account_id)
        return transactions.values('date', 'amount', 'transaction_type')
```