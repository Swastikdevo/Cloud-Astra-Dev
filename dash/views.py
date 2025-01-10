```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_overview.html', {'account': account, 'transactions': transactions})

@login_required
@require_POST
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        recipient_username = form.cleaned_data['recipient_username']
        account = Account.objects.get(user=request.user)
        recipient_account = Account.objects.get(user__username=recipient_username)

        if account.balance >= amount:
            account.balance -= amount
            recipient_account.balance += amount
            account.save()
            recipient_account.save()

            Transaction.objects.create(account=account, amount=-amount, transaction_type='transfer', recipient=recipient_account)

            return JsonResponse({'success': True, 'message': 'Transfer successful.'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient funds.'})
    return JsonResponse({'success': False, 'message': 'Invalid data.'})

@login_required
def recent_transactions(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]
    return JsonResponse({'transactions': [{'id': transaction.id, 'amount': transaction.amount, 'date': transaction.date} for transaction in transactions]})
```