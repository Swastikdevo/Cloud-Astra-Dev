```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_account = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']

            if account.balance >= amount:
                # Process the transfer
                account.balance -= amount
                recipient_account.balance += amount
                account.save()
                recipient_account.save()

                Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
                Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer', sender=account)

                return redirect('account_overview')

    else:
        form = TransferForm()

    context = {
        'account': account,
        'transactions': transactions,
        'form': form,
    }
    return render(request, 'bank/account_overview.html', context)

@require_POST
@login_required
def deposit(request):
    amount = request.POST.get('amount')
    account = Account.objects.get(user=request.user)
    account.balance += float(amount)
    account.save()

    Transaction.objects.create(account=account, amount=float(amount), transaction_type='Deposit')

    return JsonResponse({'success': True, 'new_balance': account.balance})

@require_POST
@login_required
def withdraw(request):
    amount = request.POST.get('amount')
    account = Account.objects.get(user=request.user)

    if account.balance >= float(amount):
        account.balance -= float(amount)
        account.save()

        Transaction.objects.create(account=account, amount=-float(amount), transaction_type='Withdrawal')

        return JsonResponse({'success': True, 'new_balance': account.balance})
    else:
        return JsonResponse({'success': False, 'error': 'Insufficient funds'})
```