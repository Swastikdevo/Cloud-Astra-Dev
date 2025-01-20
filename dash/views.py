```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('manage_account')
                
        elif 'create_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = Account.objects.get(id=request.POST['account_id'])
                transaction.save()
                return redirect('manage_account')

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__user=request.user)
    account_form = AccountForm()
    transaction_form = TransactionForm()

    return render(request, 'bank/manage_account.html', {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': account_form,
        'transaction_form': transaction_form,
    })

@login_required
def api_transactions(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(account__user=request.user).values('id', 'amount', 'created_at')
        return JsonResponse(list(transactions), safe=False)
```