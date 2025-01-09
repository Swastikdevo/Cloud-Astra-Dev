```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required, name='dispatch')
class BankView(View):

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
        return render(request, 'bank/home.html', {'accounts': accounts, 'transactions': transactions})

    @csrf_exempt
    def post(self, request):
        if request.POST.get("action") == "create_account":
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                return JsonResponse({'status': 'success', 'account_id': new_account.id})

        elif request.POST.get("action") == "create_transaction":
            form = TransactionForm(request.POST)
            if form.is_valid():
                new_transaction = form.save(commit=False)
                new_transaction.account = Account.objects.get(id=request.POST['account_id'])
                new_transaction.save()
                return JsonResponse({'status': 'success', 'transaction_id': new_transaction.id})

        return JsonResponse({'status': 'error', 'message': 'Invalid action or form data'})

    def delete(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id, user=request.user)
            account.delete()
            return JsonResponse({'status': 'success', 'message': 'Account deleted'})
        except Account.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found'})
```