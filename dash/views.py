```python
from django.shortcuts import render, redirect, get_object_or_404
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
            transaction = form.save(commit=False)
            transaction.account = get_object_or_404(Account, id=request.POST.get('account_id'), owner=user)
            transaction.save()
            return redirect('account_overview')

    else:
        form = TransactionForm()

    return render(request, 'bank/manage_account.html', {
        'accounts': accounts,
        'form': form,
    })

@login_required
def account_overview(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account)
    
    if request.is_ajax() and request.method == 'GET':
        data = {
            'balance': account.balance,
            'transactions': list(transactions.values('id', 'amount', 'date', 'description'))
        }
        return JsonResponse(data)

    return render(request, 'bank/account_details.html', {
        'account': account,
        'transactions': transactions,
    })
```