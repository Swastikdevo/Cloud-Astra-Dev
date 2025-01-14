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
        account_form = AccountForm()
        transaction_form = TransactionForm()
        return render(request, 'bank_management.html', {
            'accounts': accounts,
            'account_form': account_form,
            'transaction_form': transaction_form
        })

    elif request.method == 'POST':
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                new_account = account_form.save(commit=False)
                new_account.owner = request.user
                new_account.save()
                return redirect('bank_management')

        elif 'make_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'message': 'Transaction successful'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)
```