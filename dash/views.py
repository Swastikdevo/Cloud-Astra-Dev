```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, AccountForm

@login_required
def manage_accounts(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('manage_accounts')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_accounts.html', {'accounts': accounts, 'form': form})

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = form.cleaned_data['sender']
            recipient_account = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            
            # Check if sender has sufficient funds
            if sender_account.balance >= amount:
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()
                
                # Log the transaction
                Transaction.objects.create(
                    sender=sender_account,
                    recipient=recipient_account,
                    amount=amount
                )
                return JsonResponse({'success': True, 'message': 'Transfer successful!'})
            else:
                return JsonResponse({'success': False, 'message': 'Insufficient funds.'})
    else:
        form = TransferForm()

    return render(request, 'bank/transfer_funds.html', {'form': form})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(sender__user=request.user)
    return render(request, 'bank/view_transactions.html', {'transactions': transactions})
```