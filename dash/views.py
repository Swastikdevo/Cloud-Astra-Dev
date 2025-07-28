```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')[:10]
    return render(request, 'bank/dashboard.html', {'accounts': accounts, 'transactions': transactions})

@login_required
@require_POST
def create_account(request):
    account_type = request.POST.get('account_type')
    account = Account.objects.create(user=request.user, account_type=account_type)
    return JsonResponse({'status': 'success', 'account_id': account.id, 'message': 'Account created successfully.'})

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']

            # Basic validation
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                
                Transaction.objects.create(account=from_account, amount=-amount, transaction_type='transfer', to_account=to_account)
                Transaction.objects.create(account=to_account, amount=amount, transaction_type='transfer', from_account=from_account)
                
                return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form})
```