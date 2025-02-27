```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_management_view(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('account_management')
        
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return redirect('account_management')
    
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)

    account_form = AccountForm()
    transaction_form = TransactionForm()

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': account_form,
        'transaction_form': transaction_form,
    }

    return render(request, 'bank/account_management.html', context)

@login_required
def account_details_view(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

    transactions = Transaction.objects.filter(account=account)

    context = {
        'account': account,
        'transactions': transactions,
    }

    return render(request, 'bank/account_details.html', context)

@login_required
def delete_account_view(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        account.delete()
        return JsonResponse({'success': 'Account deleted successfully.'}, status=200)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
```