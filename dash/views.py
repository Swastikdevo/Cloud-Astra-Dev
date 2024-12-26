```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    """View for account management including transactions, balance inquiries, and account details."""
    
    user_account = Account.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = user_account
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction successful!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Transaction failed, please check your input.'})

    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    balance = user_account.balance

    return render(request, 'account_management.html', {
        'transactions': transactions,
        'balance': balance,
        'form': TransactionForm(),
        'account': user_account
    })
```