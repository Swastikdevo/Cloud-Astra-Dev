```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

class BankView(View):
    @login_required
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/dashboard.html', {'accounts': accounts})

    @login_required
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, pk=form.cleaned_data['account_id'], user=request.user)
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('bank:dashboard')

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, pk=form.cleaned_data['account_id'], user=request.user)
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('bank:dashboard')
                else:
                    return JsonResponse({'error': 'Insufficient balance'}, status=400)

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account = get_object_or_404(Account, pk=form.cleaned_data['from_account_id'], user=request.user)
                to_account = get_object_or_404(Account, pk=form.cleaned_data['to_account_id'])
                amount = form.cleaned_data['amount']
                if amount <= from_account.balance:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                    return redirect('bank:dashboard')
                else:
                    return JsonResponse({'error': 'Insufficient balance'}, status=400)

        return redirect('bank:dashboard')
```