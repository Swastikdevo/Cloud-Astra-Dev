```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/home.html', {'accounts': accounts})

    def post(self, request):
        action = request.POST.get('action')
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account_id = form.cleaned_data['account']
                account = get_object_or_404(Account, id=account_id, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('bank:home')

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account_id = form.cleaned_data['account']
                account = get_object_or_404(Account, id=account_id, user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
                    return redirect('bank:home')
                else:
                    return HttpResponse("Insufficient funds.")

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                source_account_id = form.cleaned_data['source_account']
                target_account_id = form.cleaned_data['target_account']
                source_account = get_object_or_404(Account, id=source_account_id, user=request.user)
                target_account = get_object_or_404(Account, id=target_account_id)

                if source_account.balance >= amount:
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    Transaction.objects.create(account=source_account, amount=-amount, transaction_type='transfer')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='transfer')
                    return redirect('bank:home')
                else:
                    return HttpResponse("Insufficient funds.")
        
        return render(request, 'bank/home.html', {'form': form})
```