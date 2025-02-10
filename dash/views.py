```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):
    template_name = 'bank_management.html'

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, self.template_name, {'accounts': accounts})

    def post(self, request):
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, id=form.cleaned_data['account_id'], user=request.user)
                account.balance += form.cleaned_data['amount']
                account.save()
                Transaction.objects.create(account=account, amount=form.cleaned_data['amount'], transaction_type='Deposit')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, id=form.cleaned_data['account_id'], user=request.user)
                if account.balance >= form.cleaned_data['amount']:
                    account.balance -= form.cleaned_data['amount']
                    account.save()
                    Transaction.objects.create(account=account, amount=form.cleaned_data['amount'], transaction_type='Withdraw')
                    return redirect('bank_management')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account = get_object_or_404(Account, id=form.cleaned_data['from_account_id'], user=request.user)
                to_account = get_object_or_404(Account, id=form.cleaned_data['to_account_id'])
                if from_account.balance >= form.cleaned_data['amount']:
                    from_account.balance -= form.cleaned_data['amount']
                    to_account.balance += form.cleaned_data['amount']
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=form.cleaned_data['amount'], transaction_type='Transfer Out')
                    Transaction.objects.create(account=to_account, amount=form.cleaned_data['amount'], transaction_type='Transfer In')
                    return redirect('bank_management')

        return render(request, self.template_name, {'error': 'Invalid operation or insufficient funds.'})
```