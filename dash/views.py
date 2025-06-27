```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@method_decorator(csrf_exempt, name='dispatch')
class BankView(View):
    def get(self, request):
        accounts = Account.objects.all()
        return render(request, 'bank/accounts_list.html', {'accounts': accounts})

    def post(self, request):
        action = request.POST.get('action')
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, id=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful', 'balance': account.balance})
            return JsonResponse({'status': 'error', 'errors': form.errors})

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, id=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful', 'balance': account.balance})
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
            return JsonResponse({'status': 'error', 'errors': form.errors})

        return JsonResponse({'status': 'error', 'message': 'Invalid operation'})

```