```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(owner=request.user)
        transactions = Transaction.objects.filter(account__in=accounts)
        account_form = AccountForm()
        transaction_form = TransactionForm()

        context = {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': account_form,
            'transaction_form': transaction_form
        }
        return render(request, 'bank_management.html', context)

    elif request.method == 'POST':
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                new_account = account_form.save(commit=False)
                new_account.owner = request.user
                new_account.save()
                return redirect('bank_management')

        elif 'create_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                new_transaction = transaction_form.save(commit=False)
                new_transaction.account = Account.objects.get(id=request.POST['account_id'])
                new_transaction.save()
                return redirect('bank_management')

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
```