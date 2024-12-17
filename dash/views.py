```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.owner = request.user
                account.save()
                return redirect('account_list')
        
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'success': True, 'transaction_id': transaction.id})

    else:
        account_form = AccountForm()
        transaction_form = TransactionForm()
    
    accounts = Account.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'account_form': account_form,
        'transaction_form': transaction_form,
        'accounts': accounts,
        'transactions': transactions,
    }
    return render(request, 'bank/manage_account.html', context)
```