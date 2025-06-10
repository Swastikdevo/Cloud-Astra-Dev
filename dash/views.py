```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/account_overview.html', context)

@login_required
@require_POST
def transfer_money(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        recipient_username = form.cleaned_data['recipient']
        
        try:
            recipient = Account.objects.get(user__username=recipient_username)
            account = Account.objects.get(user=request.user)
            
            if account.balance >= amount:
                account.balance -= amount
                recipient.balance += amount
                account.save()
                recipient.save()
                
                Transaction.objects.create(
                    account=account,
                    amount=-amount,
                    transaction_type='Transfer',
                    description=f'Transferred {amount} to {recipient_username}'
                )
                Transaction.objects.create(
                    account=recipient,
                    amount=amount,
                    transaction_type='Transfer',
                    description=f'Received {amount} from {request.user.username}'
                )
                
                messages.success(request, f'Successfully transferred {amount} to {recipient_username}')
            else:
                messages.error(request, 'Insufficient funds for this transaction.')
        except Account.DoesNotExist:
            messages.error(request, 'Recipient account does not exist.')
    else:
        messages.error(request, 'Invalid transfer details.')

    return redirect('account_overview')

@login_required
def get_account_balance(request):
    account = Account.objects.get(user=request.user)
    return JsonResponse({'balance': account.balance})
```