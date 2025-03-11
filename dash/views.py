```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def account_overview(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@csrf_exempt
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_username = form.cleaned_data['recipient']
            accounts = Account.objects.filter(owner=request.user)

            if amount <= 0:
                return JsonResponse({'error': 'Amount must be greater than zero.'}, status=400)

            if not accounts.exists():
                return JsonResponse({'error': 'No accounts found.'}, status=400)

            try:
                recipient_user = User.objects.get(username=recipient_username)
                recipient_account = Account.objects.get(owner=recipient_user)
                sender_account = accounts.first()  # Assuming one account per user for simplicity

                if sender_account.balance < amount:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

                # Perform transfer
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()

                # Log transaction
                Transaction.objects.create(
                    sender=sender_account,
                    recipient=recipient_account,
                    amount=amount
                )

                return JsonResponse({'message': 'Transfer successful!'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Recipient not found.'}, status=404)
            except Account.DoesNotExist:
                return JsonResponse({'error': 'Recipient account not found.'}, status=404)
    else:
        form = TransferForm()

    return render(request, 'bank/transfer_funds.html', {'form': form})

@login_required
def transaction_history(request):
    user = request.user
    transactions = Transaction.objects.filter(sender__owner=user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```