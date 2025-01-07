```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = Account.objects.get(user=request.user)
            receiver_account = Account.objects.get(account_number=form.cleaned_data['account_number'])
            amount = form.cleaned_data['amount']

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()
                
                # Log the transaction
                Transaction.objects.create(
                    sender=sender_account,
                    receiver=receiver_account,
                    amount=amount,
                    description=f'Transferred {amount} to {receiver_account.account_number}'
                )
                
                return JsonResponse({'status': 'success', 'message': 'Transfer completed!'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'}, status=400)
    else:
        form = TransferForm()
    
    return render(request, 'transfer_funds.html', {'form': form})
```