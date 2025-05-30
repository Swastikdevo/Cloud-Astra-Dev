```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import BankAccount, Transaction
from .forms import DepositForm, WithdrawalForm

@method_decorator(login_required, name='dispatch')
class BankAccountView(View):
    def get(self, request):
        accounts = BankAccount.objects.filter(owner=request.user)
        return render(request, 'bank/account_list.html', {'accounts': accounts})

    def post(self, request):
        action_type = request.POST.get('action')
        if action_type == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(BankAccount, id=form.cleaned_data['account_id'], owner=request.user)
                account.balance += form.cleaned_data['amount']
                account.save()
                Transaction.objects.create(account=account, amount=form.cleaned_data['amount'], transaction_type='deposit')
                return redirect('bank:account_list')

        elif action_type == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(BankAccount, id=form.cleaned_data['account_id'], owner=request.user)
                if account.balance >= form.cleaned_data['amount']:
                    account.balance -= form.cleaned_data['amount']
                    account.save()
                    Transaction.objects.create(account=account, amount=form.cleaned_data['amount'], transaction_type='withdrawal')
                else:
                    return HttpResponse("Insufficient funds!")

                return redirect('bank:account_list')

        return render(request, 'bank/account_list.html', {'error': 'Invalid action or form data.'})

```