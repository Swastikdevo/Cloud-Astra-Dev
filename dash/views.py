```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required, name='dispatch')
class BankView(View):
    template_name = 'bank/index.html'

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, self.template_name, {'accounts': accounts})

    def post(self, request):
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('bank:index')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('bank:index')
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

        return render(request, self.template_name, {'accounts': Account.objects.filter(user=request.user)})
```