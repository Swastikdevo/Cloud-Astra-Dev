```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_overview.html', {'account': account, 'transactions': transactions})

@login_required
@require_POST
def make_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = Account.objects.get(user=request.user)
        transaction.save()
        return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid transaction data.'})

@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

def dashboard(request):
    if request.user.is_authenticated:
        return redirect('account_overview')
    return render(request, 'bank/dashboard.html')
```