```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'account_overview.html', {'accounts': user_accounts})

@login_required
@csrf_exempt
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            source_account = form.cleaned_data['source_account']
            target_account = form.cleaned_data['target_account']
            amount = form.cleaned_data['amount']

            if source_account.balance >= amount:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()
                Transaction.objects.create(
                    source_account=source_account,
                    target_account=target_account,
                    amount=amount
                )
                return JsonResponse({'status': 'success', 'message': 'Transfer successful.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    form = TransferForm()
    return render(request, 'transfer_funds.html', {'form': form})

@login_required
def transaction_history(request):
    user_accounts = Account.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(source_account__owner=request.user) | Transaction.objects.filter(target_account__owner=request.user)
    return render(request, 'transaction_history.html', {'transactions': transactions.distinct()})
```