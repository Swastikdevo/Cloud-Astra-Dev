```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@method_decorator(login_required, name='dispatch')
class BankView(View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/home.html', {'accounts': accounts})

    def post(self, request):
        action = request.POST.get('action')
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=request.POST.get('account_id'), user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
        
        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=request.POST.get('account_id'), user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'status': 'success', 'new_balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid action'})
```