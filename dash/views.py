```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@login_required
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
        return render(request, 'bank/manage.html', {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm()
        })

    elif request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                return JsonResponse({'success': True, 'message': 'Account created successfully.'})
        elif 'create_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                new_transaction = form.save(commit=False)
                new_transaction.account = Account.objects.get(id=request.POST.get('account_id'))
                new_transaction.save()
                return JsonResponse({'success': True, 'message': 'Transaction recorded successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})
```