```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    """View to manage bank account - Deposit, Withdraw, and View Transactions."""
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('account_overview')
                
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return redirect('account_overview')
                else:
                    error_message = "Insufficient funds."
                    return render(request, 'account/manage_account.html', {'withdrawal_form': form, 'error_message': error_message})

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    
    return render(request, 'account/manage_account.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    })

@require_POST
@login_required
def delete_transaction(request, transaction_id):
    """View to delete a specific transaction."""
    try:
        transaction = Transaction.objects.get(id=transaction_id, account__user=request.user)
        transaction.delete()
        return JsonResponse({'status': 'success', 'message': 'Transaction deleted successfully.'})
    except Transaction.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Transaction not found.'}, status=404)
```