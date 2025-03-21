```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']
            
            # Check for sufficient funds for withdrawal
            if transaction_type == 'withdrawal' and user_account.balance < amount:
                messages.error(request, "Insufficient funds.")
                return redirect('manage_account')
            
            # Create a new transaction
            transaction = Transaction.objects.create(
                account=user_account,
                amount=amount,
                transaction_type=transaction_type
            )
            user_account.balance += amount if transaction_type == 'deposit' else -amount
            user_account.save()
            messages.success(request, f"Transaction successful: {transaction_type} of ${amount}.")
            return redirect('manage_account')
    
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-date_created')
    return render(request, 'bank/manage_account.html', {
        'form': form,
        'balance': user_account.balance,
        'transactions': transactions
    })

@login_required
def transaction_history(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date_created')
    return render(request, 'bank/transaction_history.html', {
        'transactions': transactions
    })
```