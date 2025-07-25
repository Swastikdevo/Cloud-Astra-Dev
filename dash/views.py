```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        if 'add_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.owner = request.user
                new_account.save()
                return redirect('bank_dashboard')
        
        elif 'add_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                new_transaction = form.save(commit=False)
                new_transaction.account = Account.objects.get(id=request.POST['account_id'])
                new_transaction.save()
                return redirect('bank_dashboard')

    context = {
        'accounts': user_accounts,
        'transaction_form': TransactionForm(),
        'account_form': AccountForm(),
    }
    return render(request, 'bank/dashboard.html', context)

@login_required
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})

@login_required
def api_balance(request, account_id):
    account = Account.objects.get(id=account_id)
    if account.owner != request.user:
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

    return JsonResponse({'balance': account.balance})
```