```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(id=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful.')
                return redirect('manage_account')

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(id=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful.')
                else:
                    messages.error(request, 'Insufficient balance.')
                return redirect('manage_account')

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                source_account = Account.objects.get(id=form.cleaned_data['source_account_id'])
                target_account = Account.objects.get(id=form.cleaned_data['target_account_id'])
                amount = form.cleaned_data['amount']
                if source_account.balance >= amount:
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    Transaction.objects.create(account=source_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, 'Transfer successful.')
                else:
                    messages.error(request, 'Insufficient balance.')
                return redirect('manage_account')

    return HttpResponse(status=405)
```