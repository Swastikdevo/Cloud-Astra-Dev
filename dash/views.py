```python
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
@csrf_exempt
def bank_dashboard(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/dashboard.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            messages.success(request, 'New account created successfully!')
            return redirect('bank_dashboard')
        else:
            messages.error(request, 'Error creating account. Please try again.')

    return HttpResponseBadRequest("Invalid request method.")


@login_required
@csrf_exempt
def perform_transaction(request, account_id):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=account_id, user=request.user)
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return JsonResponse({'status': 'success', 'message': 'Transaction Completed!'})
        else:
            messages.error(request, 'Error processing transaction. Please check your input.')

    return JsonResponse({'status': 'error', 'message': 'Invalid transaction data!'}, status=400)


@login_required
def view_account_details(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/account_details.html', {'account': account, 'transactions': transactions})
```