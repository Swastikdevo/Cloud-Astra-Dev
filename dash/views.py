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
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = Account.objects.get(user=request.user)
            recipient_account = Account.objects.get(account_number=form.cleaned_data['recipient_account_number'])
            amount = form.cleaned_data['amount']

            if amount <= 0:
                return JsonResponse({"error": "Amount must be greater than zero."}, status=400)
            if sender_account.balance < amount:
                return JsonResponse({"error": "Insufficient funds."}, status=400)

            # Process the transfer
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()

            # Create a transaction record
            Transaction.objects.create(
                sender=sender_account,
                recipient=recipient_account,
                amount=amount
            )

            return JsonResponse({"success": "Transfer completed successfully."})

    else:
        form = TransferForm()

    return render(request, 'transfer_funds.html', {'form': form})
```