```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def transfer_money(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        sender_account = Account.objects.get(pk=form.cleaned_data['sender_account'])
        receiver_account = Account.objects.get(pk=form.cleaned_data['receiver_account'])
        amount = form.cleaned_data['amount']

        if sender_account.balance >= amount:
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()

            Transaction.objects.create(
                sender=sender_account,
                receiver=receiver_account,
                amount=amount,
                description=form.cleaned_data['description']
            )
            return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid data.'})

@login_required
def account_details(request, account_id):
    account = Account.objects.get(pk=account_id, user=request.user)
    transactions = Transaction.objects.filter(sender=account) | Transaction.objects.filter(receiver=account)
    return render(request, 'bank/account_details.html', {'account': account, 'transactions': transactions})
```