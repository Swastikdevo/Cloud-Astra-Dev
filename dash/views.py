```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})

    accounts = Account.objects.filter(owner=request.user)
    form = AccountForm()
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})

    form = TransactionForm()
    return render(request, 'bank/make_transaction.html', {'form': form})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```