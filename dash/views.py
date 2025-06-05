```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account
from .forms import AccountForm, TransferForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_overview')
    else:
        form = AccountForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def transfer_funds(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST, instance=account)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_account_id = form.cleaned_data['recipient_account']
            recipient_account = get_object_or_404(Account, id=recipient_account_id)

            if account.balance >= amount:
                account.balance -= amount
                recipient_account.balance += amount
                account.save()
                recipient_account.save()
                messages.success(request, 'Transfer successful!')
                return redirect('account_overview')
            else:
                messages.error(request, 'Insufficient funds.')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer_funds.html', {'form': form, 'account': account})

@login_required
def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    return render(request, 'bank/account_details.html', {'account': account})
```