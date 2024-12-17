```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    context = {
        'accounts': accounts,
        'transaction_form': TransactionForm(),
    }
    return render(request, 'bank/account_overview.html', context)

@login_required
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        return JsonResponse({'success': True, 'message': 'Account created successfully!'})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def create_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        return JsonResponse({'success': True, 'message': 'Transaction recorded successfully!'})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```