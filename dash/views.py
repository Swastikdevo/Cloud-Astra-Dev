```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import CreateAccountForm, TransferForm

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == "POST":
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_dashboard')
    else:
        form = CreateAccountForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def transfer_funds(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = form.cleaned_data['sender_account']
            recipient_account = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                recipient_account.balance += amount
                Transaction.objects.create(
                    sender=sender_account,
                    recipient=recipient_account,
                    amount=amount
                )
                sender_account.save()
                recipient_account.save()
                messages.success(request, 'Transfer completed successfully!')
                return redirect('account_dashboard')
            else:
                messages.error(request, 'Insufficient balance for this transfer.')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer_funds.html', {'form': form})
```