```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import TransferForm

@login_required
@csrf_exempt
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = Account.objects.get(user=request.user)
            recipient_account = Account.objects.get(account_number=form.cleaned_data['recipient_account_number'])
            amount = form.cleaned_data['amount']

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
                return JsonResponse({'message': 'Transfer successful'}, status=200)
            else:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
        return JsonResponse({'error': 'Invalid form'}, status=400)
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form})
```