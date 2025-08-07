```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_overview')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'success': True, 'message': 'Transaction recorded successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_view.html', {'form': TransactionForm(), 'transactions': transactions})
```