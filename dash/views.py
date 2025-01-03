```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@require_http_methods(['GET', 'POST'])
def bank_management_view(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('bank_management_view')
        
        elif 'make_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                account = Account.objects.get(id=request.POST['account_id'])
                transaction.account = account
                transaction.save()
                return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    
    else:
        accounts = Account.objects.all()
        transactions = Transaction.objects.all()
        account_form = AccountForm()
        transaction_form = TransactionForm()
        
    return render(request, 'bank_management.html', {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': account_form,
        'transaction_form': transaction_form,
    })
```