```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm

@login_required
@require_http_methods(["GET", "POST"])
def bank_management_view(request):
    if request.method == "POST":
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            sender_account = Account.objects.get(user=request.user)
            recipient_account = Account.objects.get(account_number=transfer_form.cleaned_data['recipient'])
            amount = transfer_form.cleaned_data['amount']

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()

                # Record the transaction
                Transaction.objects.create(
                    sender=sender_account,
                    recipient=recipient_account,
                    amount=amount,
                    description=transfer_form.cleaned_data.get('description', '')
                )
                return JsonResponse({"status": "success", "message": "Transfer completed successfully!"})
            else:
                return JsonResponse({"status": "error", "message": "Insufficient balance."})

    else:
        transfer_form = TransferForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank_management.html', {
        'transfer_form': transfer_form,
        'accounts': accounts
    })
```