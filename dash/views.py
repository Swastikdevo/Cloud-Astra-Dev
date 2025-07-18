```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def account_overview(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'POST':
        # Create a new transaction
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

    else:
        transaction_form = TransactionForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')
    context = {
        'account': account,
        'transactions': transactions,
        'transaction_form': transaction_form,
    }

    return render(request, 'account_overview.html', context)

@login_required
@csrf_exempt
def create_account(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_form.save()
            return redirect('account_list')

    else:
        account_form = AccountForm()

    return render(request, 'create_account.html', {'account_form': account_form})

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'account_list.html', {'accounts': accounts})
```