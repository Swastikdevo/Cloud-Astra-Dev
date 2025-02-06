```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
        return render(request, 'bank_management.html', {'accounts': accounts, 'transactions': transactions})

    def post(self, request):
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('bank_management')
        
        elif 'create_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return redirect('bank_management')

        return JsonResponse({'error': 'Invalid action'}, status=400)

    def delete_account(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id, user=request.user)
            account.delete()
            return JsonResponse({'message': 'Account deleted successfully'})
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)

    def update_transaction(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            if request.user == transaction.user:
                form = TransactionForm(request.POST, instance=transaction)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'message': 'Transaction updated successfully'})
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found'}, status=404)
```