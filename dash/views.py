```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.views import View

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts)

        return render(request, 'bank_management/dashboard.html', {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm()
        })

    def post(self, request):
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                new_account = account_form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                return redirect('bank_management:dashboard')
        
        elif 'create_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.account = transaction_form.cleaned_data['account']
                transaction.save()
                return redirect('bank_management:dashboard')

        return self.get(request)

    def ajax_get_account_details(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id, user=request.user)
            return JsonResponse({
                'account_number': account.account_number,
                'balance': account.balance,
                'account_type': account.account_type,
            })
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found.'}, status=404)

    def ajax_get_transaction_history(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id, user=request.user)
            transactions = Transaction.objects.filter(account=account)
            transaction_data = [
                {
                    'id': transaction.id,
                    'amount': transaction.amount,
                    'date': transaction.date,
                    'type': transaction.transaction_type,
                }
                for transaction in transactions
            ]
            return JsonResponse(transaction_data, safe=False)

        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found.'}, status=404)
```