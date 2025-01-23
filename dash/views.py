```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

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

    return JsonResponse({'error': 'Invalid data'}, status=400)

@login_required
@csrf_exempt
def record_transaction(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(account__user=request.user)
        form = TransactionForm()
        return render(request, 'bank/record_transaction.html', {'transactions': transactions, 'form': form})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=request.POST.get('account_id'), user=request.user)
            transaction.save()
            return redirect('record_transaction')

    return JsonResponse({'error': 'Invalid data'}, status=400)
```