```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm

@login_required
@require_http_methods(["GET", "POST"])
def bank_management_view(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = request.user.account
                receiver_account = form.cleaned_data['receiver_account']
                amount = form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    Transaction.objects.create(
                        sender=sender_account,
                        receiver=receiver_account,
                        amount=amount,
                        description=form.cleaned_data['description']
                    )
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                
        elif 'create_account' in request.POST:
            form = AccountCreationForm(request.POST)
            if form.is_valid():
                Account.objects.create(
                    user=form.cleaned_data['user'],
                    initial_balance=form.cleaned_data['initial_balance']
                )
                messages.success(request, 'Account created successfully!')
            else:
                messages.error(request, 'Account creation failed!')

    transfer_form = TransferForm()
    accounts = Account.objects.filter(user=request.user)

    return render(request, 'bank_management.html', {
        'transfer_form': transfer_form,
        'accounts': accounts,
    })
```