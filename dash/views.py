```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from .forms import BankAccountForm, TransactionForm

@csrf_exempt
@login_required
def bank_account_view(request):
    if request.method == 'GET':
        accounts = BankAccount.objects.filter(user=request.user)
        form = BankAccountForm()
        return render(request, 'bank/account_view.html', {'accounts': accounts, 'form': form})

    elif request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'success': True, 'message': 'Account created successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

@csrf_exempt
@login_required
def transaction_view(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(account__user=request.user)
        form = TransactionForm()
        return render(request, 'bank/transaction_view.html', {'transactions': transactions, 'form': form})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.save()
            return JsonResponse({'success': True, 'message': 'Transaction recorded successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def generate_statement(request, account_id):
    account = BankAccount.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/statement.html', {'account': account, 'transactions': transactions})
```