```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm

@login_required
@require_http_methods(["GET", "POST"])
def bank_view(request):
    if request.method == "POST":
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender_account = Account.objects.get(user=request.user)
                receiver_account = Account.objects.get(account_number=transfer_form.cleaned_data['receiver_account'])
                amount = transfer_form.cleaned_data['amount']

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
                    return redirect('bank_view')
                else:
                    return HttpResponse("Insufficient funds.")

        elif 'create_account' in request.POST:
            account_form = AccountCreationForm(request.POST)
            if account_form.is_valid():
                new_account = account_form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                return redirect('bank_view')

    transfer_form = TransferForm()
    account_form = AccountCreationForm()
    accounts = Account.objects.filter(user=request.user)

    return render(request, 'bank_view.html', {
        'transfer_form': transfer_form,
        'account_form': account_form,
        'accounts': accounts,
    })
```