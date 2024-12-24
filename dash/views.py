```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction_type = form.cleaned_data['transaction_type']
            amount = form.cleaned_data['amount']
            account_id = form.cleaned_data['account'].id
            
            account = Account.objects.get(id=account_id, owner=user)
            if transaction_type == 'deposit':
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, transaction_type='deposit', amount=amount)
                return JsonResponse({'status': 'success', 'message': 'Deposit successful'})
            elif transaction_type == 'withdrawal':
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, transaction_type='withdrawal', amount=amount)
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    
    form = TransactionForm()
    context = {
        'accounts': accounts,
        'form': form,
    }
    return render(request, 'bank/manage_account.html', context)
```