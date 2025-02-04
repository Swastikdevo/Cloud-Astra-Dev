```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def transfer_funds(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = request.user.account
            recipient_account = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']

            if sender_account.balance >= amount:
                # Create a new transaction
                Transaction.objects.create(
                    sender=sender_account,
                    recipient=recipient_account,
                    amount=amount
                )

                # Update balances
                sender_account.balance -= amount
                recipient_account.balance += amount
                
                sender_account.save()
                recipient_account.save()
                return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'}, status=400)
    else:
        form = TransferForm()

    return render(request, 'bank/transfer_funds.html', {'form': form})
```