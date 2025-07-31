```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_account_number = form.cleaned_data['recipient_account_number']
            
            try:
                sender_account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.get(account_number=recipient_account_number)
                
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    
                    Transaction.objects.create(
                        sender=sender_account,
                        recipient=recipient_account,
                        amount=amount,
                        transaction_type='Transfer'
                    )
                    
                    messages.success(request, f'Transferred ${amount} to account {recipient_account_number} successfully.')
                else:
                    messages.error(request, 'Insufficient funds in your account.')
                    
            except Account.DoesNotExist:
                messages.error(request, 'Recipient account does not exist.')
            
            return redirect('transfer_funds')
    else:
        form = TransferForm()
    
    return render(request, 'bank/transfer_funds.html', {'form': form})
```