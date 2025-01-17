```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm

@login_required
def bank_management_view(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountCreationForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.owner = user
                new_account.save()
                messages.success(request, 'New account created successfully!')
                return redirect('bank_management')

        elif 'transfer_funds' in request.POST:
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

                    Transaction.objects.create(
                        sender=sender_account,
                        receiver=receiver_account,
                        amount=amount
                    )
                    messages.success(request, 'Funds transferred successfully!')
                else:
                    messages.error(request, 'Insufficient funds for this transaction.')
                return redirect('bank_management')

    context = {
        'accounts': accounts,
        'transfer_form': TransferForm(),
        'account_creation_form': AccountCreationForm(),
    }
    return render(request, 'bank_management.html', context)
```