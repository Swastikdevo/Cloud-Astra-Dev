```python
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@method_decorator(login_required, name='dispatch')
class BankAccountView(View):
    template_name = 'bank/account.html'

    def get(self, request):
        account = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(account=account).order_by('-date')
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        return render(request, self.template_name, {
            'account': account,
            'transactions': transactions,
            'deposit_form': deposit_form,
            'withdraw_form': withdraw_form
        })

    def post(self, request):
        account = Account.objects.get(user=request.user)
        
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('bank:account')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds!')
                else:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                return redirect('bank:account')

        messages.error(request, 'There was an error processing your request.')
        return redirect('bank:account')
```