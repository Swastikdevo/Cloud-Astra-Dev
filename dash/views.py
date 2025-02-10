```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import CreateAccountForm, TransactionForm
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                messages.success(request, 'Account created successfully!')
                return redirect('manage_account')
        
        elif 'perform_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = get_object_or_404(Account, pk=request.POST['account_id'])
                transaction.save()
                messages.success(request, 'Transaction completed successfully!')
                return redirect('manage_account')
            
    else:
        create_account_form = CreateAccountForm()
        transaction_form = TransactionForm()
        accounts = Account.objects.filter(user=request.user)
    
    context = {
        'create_account_form': create_account_form,
        'transaction_form': transaction_form,
        'accounts': accounts,
    }
    
    return render(request, 'bank/manage_account.html', context)

@login_required
@require_http_methods(["GET"])
def account_details(request, account_id):
    account = get_object_or_404(Account, pk=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    
    context = {
        'account': account,
        'transactions': transactions
    }
    
    return render(request, 'bank/account_details.html', context)

@login_required
@require_http_methods(["DELETE"])
def delete_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id, user=request.user)
    account.delete()
    return JsonResponse({'message': 'Account deleted successfully!'})
```