```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    user = request.user
    account = get_object_or_404(Account, user=user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()

            # Implementing new feature: Transaction History Update
            account.transaction_history.append(transaction.id)
            account.save()

            return redirect('account_detail')
    else:
        form = TransactionForm()

    # New Feature: Displaying account balance and recent transactions
    recent_transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]
    context = {
        'account': account,
        'form': form,
        'recent_transactions': recent_transactions,
    }

    return render(request, 'manage_account.html', context)

@login_required
def account_balance(request):
    user = request.user
    account = get_object_or_404(Account, user=user)
    
    # New Feature: Real-time balance updates via AJAX
    if request.is_ajax():
        return JsonResponse({'balance': account.balance})

    return redirect('manage_account')
```