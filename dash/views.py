```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_view(request):
    accounts = Account.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_view')
    else:
        form = AccountForm()

    return render(request, 'bank/account_view.html', {
        'accounts': accounts,
        'form': form,
    })

@login_required
@require_POST
def transaction_view(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        return JsonResponse({'status': 'success', 'message': 'Transaction successful'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid transaction data'})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {
        'transactions': transactions,
    })
```