```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            return handle_deposit(request, account)
        elif 'withdraw' in request.POST:
            return handle_withdraw(request, account)
        elif 'transfer' in request.POST:
            return handle_transfer(request, account)

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'account_overview.html', context)

@require_POST
@login_required
def handle_deposit(request, account):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return redirect('account_overview')
    return JsonResponse({'error': form.errors}, status=400)

@require_POST
@login_required
def handle_withdraw(request, account):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return redirect('account_overview')
        else:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)
    return JsonResponse({'error': form.errors}, status=400)

@require_POST
@login_required
def handle_transfer(request, account):
    form = TransferForm(request.POST)
    if form.is_valid():
        recipient_username = form.cleaned_data['recipient']
        amount = form.cleaned_data['amount']
        if account.balance >= amount:
            recipient_account = Account.objects.get(user__username=recipient_username)
            account.balance -= amount
            recipient_account.balance += amount
            account.save()
            recipient_account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
            return redirect('account_overview')
        else:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)
    return JsonResponse({'error': form.errors}, status=400)
```