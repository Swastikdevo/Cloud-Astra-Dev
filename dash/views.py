```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required
def account_overview(request):
    """Display account overview for the logged-in user."""
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank_management/account_overview.html', {'accounts': user_accounts})

@login_required
@require_POST
def transfer_funds(request):
    """Transfer funds between accounts."""
    source_account_id = request.POST.get('source_account')
    target_account_id = request.POST.get('target_account')
    amount = float(request.POST.get('amount'))

    source_account = Account.objects.get(id=source_account_id)
    target_account = Account.objects.get(id=target_account_id)

    if source_account.balance >= amount:
        source_account.balance -= amount
        target_account.balance += amount
        source_account.save()
        target_account.save()

        # Create transaction record
        Transaction.objects.create(
            from_account=source_account,
            to_account=target_account,
            amount=amount,
            description=f'Transferred {amount} from {source_account} to {target_account}'
        )

        messages.success(request, 'Funds transferred successfully!')
    else:
        messages.error(request, 'Insufficient funds in source account.')

    return redirect('account_overview')

@login_required
def account_statement(request, account_id):
    """Display transaction history for a specific account."""
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(from_account=account) | Transaction.objects.filter(to_account=account)

    return render(request, 'bank_management/account_statement.html', {
        'account': account,
        'transactions': transactions.order_by('-date')
    })
```