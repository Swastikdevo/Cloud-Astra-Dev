```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_overview')
    else:
        form = AccountCreationForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            source_account = get_object_or_404(Account, id=form.cleaned_data['source_account_id'], user=request.user)
            target_account = get_object_or_404(Account, id=form.cleaned_data['target_account_id'])
            amount = form.cleaned_data['amount']

            if source_account.balance >= amount:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()

                # Log the transaction
                Transaction.objects.create(
                    source_account=source_account,
                    target_account=target_account,
                    amount=amount,
                    user=request.user
                )
                return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds in source account.'})
    else:
        form = TransferForm()
    return render(request, 'bank/transfer_funds.html', {'form': form})
```