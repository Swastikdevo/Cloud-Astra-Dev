```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm

@require_http_methods(["GET", "POST"])
@login_required
def transfer_money(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = Account.objects.get(user=request.user)
            recipient_account = Account.objects.get(account_number=form.cleaned_data['recipient_account_number'])
            amount = form.cleaned_data['amount']

            if sender_account.balance >= amount:
                # Create transaction for the sender
                Transaction.objects.create(
                    account=sender_account,
                    amount=-amount,
                    transaction_type='debit',
                    description=f'Transferred {amount} to {recipient_account.user.username}'
                )
                # Create transaction for the recipient
                Transaction.objects.create(
                    account=recipient_account,
                    amount=amount,
                    transaction_type='credit',
                    description=f'Received {amount} from {sender_account.user.username}'
                )
                
                # Update balances
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()

                return JsonResponse({'status': 'success', 'message': 'Transfer successful!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data.'})

    else:
        form = TransferForm()

    return render(request, 'transfer.html', {'form': form})
```