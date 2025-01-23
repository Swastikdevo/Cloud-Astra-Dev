```python
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):
    template_name = 'bank_management.html'

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')[:10]
        context = {
            'accounts': accounts,
            'transactions': transactions,
            'deposit_form': DepositForm(),
            'withdrawal_form': WithdrawalForm(),
            'transfer_form': TransferForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                deposit_amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(id=request.POST['account_id'])
                account.balance += deposit_amount
                account.save()
                Transaction.objects.create(account=account, amount=deposit_amount, transaction_type='Deposit')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                withdrawal_amount = withdrawal_form.cleaned_data['amount']
                account = Account.objects.get(id=request.POST['account_id'])
                if account.balance >= withdrawal_amount:
                    account.balance -= withdrawal_amount
                    account.save()
                    Transaction.objects.create(account=account, amount=withdrawal_amount, transaction_type='Withdrawal')
                    return redirect('bank_management')

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                transfer_amount = transfer_form.cleaned_data['amount']
                from_account = Account.objects.get(id=request.POST['from_account_id'])
                to_account = Account.objects.get(id=request.POST['to_account_id'])
                if from_account.balance >= transfer_amount:
                    from_account.balance -= transfer_amount
                    to_account.balance += transfer_amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=transfer_amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=to_account, amount=transfer_amount, transaction_type='Transfer In')
                    return redirect('bank_management')

        return redirect('bank_management')
```