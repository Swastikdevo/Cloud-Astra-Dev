```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_detail(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('account_detail')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return redirect('account_detail')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'account_detail.html', context)

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        sender_account = Account.objects.get(user=request.user)
        recipient_id = request.POST.get('recipient_id')
        amount = float(request.POST.get('amount'))

        recipient_account = Account.objects.get(id=recipient_id)
        
        if amount <= sender_account.balance:
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()
            Transaction.objects.create(account=sender_account, amount=amount, transaction_type='transfer_out')
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in')
            return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds for transfer.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
```