```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = request.user.account
            amount = form.cleaned_data['amount']
            recipient_account_number = form.cleaned_data['recipient_account_number']
            recipient_account = Account.objects.filter(account_number=recipient_account_number).first()

            if not recipient_account:
                return JsonResponse({'error': 'Recipient account not found.'}, status=404)
            if sender_account.balance < amount:
                return JsonResponse({'error': 'Insufficient funds.'}, status=400)

            # Perform the transfer
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()

            # Create transaction records
            Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='transfer', recipient=recipient_account)
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='receive', sender=sender_account)

            return JsonResponse({'success': 'Funds transferred successfully.'})

    else:
        form = TransferForm()

    return render(request, 'bank/transfer_funds.html', {'form': form})
```