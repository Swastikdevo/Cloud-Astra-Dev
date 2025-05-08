```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                messages.success(request, 'Account created successfully!')
                return redirect('manage_account')
        elif 'transfer_funds' in request.POST:
            transfer_form = TransactionForm(request.POST)
            if transfer_form.is_valid():
                transaction = transfer_form.save(commit=False)
                transaction.sender = request.user.account  # Assuming account relation with user
                transaction.save()
                messages.success(request, 'Funds transferred successfully!')
                return redirect('manage_account')

    accounts = Account.objects.filter(user=request.user)
    account_form = AccountForm()
    transfer_form = TransactionForm()

    return render(request, 'bank/manage_account.html', {
        'accounts': accounts,
        'account_form': account_form,
        'transfer_form': transfer_form,
    })
```