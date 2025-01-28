```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm
from django.contrib import messages

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        sender_account = form.cleaned_data['sender_account']
        receiver_account = form.cleaned_data['receiver_account']
        amount = form.cleaned_data['amount']
        
        if sender_account.balance >= amount:
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()
            
            transaction = Transaction(
                sender=sender_account,
                receiver=receiver_account,
                amount=amount,
                user=request.user
            )
            transaction.save()

            messages.success(request, 'Transfer successful!')
            return redirect('account_dashboard')
        else:
            messages.error(request, 'Insufficient funds!')
    else:
        messages.error(request, 'Invalid transfer data!')

    return redirect('account_dashboard')
```