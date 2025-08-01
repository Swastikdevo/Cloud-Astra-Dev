```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        form = AccountForm()
        return render(request, 'bank/manage_account.html', {'accounts': accounts, 'form': form})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('manage_account')

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'success': 'Transaction successful'}, status=200)

    return JsonResponse({'error': 'Invalid request, transaction not processed'}, status=400)

@login_required
@csrf_exempt
def account_summary(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'bank/account_summary.html', {'account': account, 'transactions': transactions})
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
```