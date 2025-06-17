```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': user_accounts})

class TransactionView(View):
    def get(self, request):
        transactions = Transaction.objects.filter(account__owner=request.user).order_by('-date')
        return render(request, 'bank/transaction_history.html', {'transactions': transactions})

    @login_required
    def post(self, request):
        action = request.POST.get('action')
        account = Account.objects.get(id=request.POST.get('account_id'), owner=request.user)

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'balance': account.balance})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'success': True, 'balance': account.balance})
                else:
                    return JsonResponse({'success': False, 'error': 'Insufficient funds'})

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                target_account = Account.objects.get(id=form.cleaned_data['target_account_id'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    target_account.balance += amount
                    account.save()
                    target_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                    return JsonResponse({'success': True, 'balance': account.balance})
                else:
                    return JsonResponse({'success': False, 'error': 'Insufficient funds'})

        return JsonResponse({'success': False, 'error': 'Invalid action'})
```