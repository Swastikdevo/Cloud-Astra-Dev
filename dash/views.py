```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank_dashboard.html', {'accounts': user_accounts})

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            sender_account = form.cleaned_data['sender_account']
            recipient_account = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()

                Transaction.objects.create(
                    sender=sender_account,
                    recipient=recipient_account,
                    amount=amount
                )
                return JsonResponse({'status': 'success', 'message': 'Transfer successful.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    else:
        form = TransactionForm()
    return render(request, 'transfer_funds.html', {'form': form})

@login_required
def transaction_history(request):
    user_transactions = Transaction.objects.filter(sender__owner=request.user) | Transaction.objects.filter(recipient__owner=request.user)
    return render(request, 'transaction_history.html', {'transactions': user_transactions})
```