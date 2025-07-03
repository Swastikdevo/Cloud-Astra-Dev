```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Account, Transaction
from .forms import AccountForm

@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        return render(request, 'bank/accounts.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            return JsonResponse({'message': 'Account created successfully', 'account_id': account.id}, status=201)
        return JsonResponse({'error': form.errors}, status=400)

@csrf_exempt
def transaction_history(request, account_id):
    if request.method == 'GET':
        try:
            account = Account.objects.get(id=account_id)
            transactions = Transaction.objects.filter(account=account)
            return render(request, 'bank/transactions.html', {'account': account, 'transactions': transactions})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)

@csrf_exempt
def make_transaction(request, account_id):
    if request.method == 'POST':
        try:
            account = Account.objects.get(id=account_id)
            amount = float(request.POST.get('amount', 0))
            transaction_type = request.POST.get('type', None)

            if transaction_type not in ['deposit', 'withdraw']:
                return JsonResponse({'error': 'Invalid transaction type'}, status=400)

            if transaction_type == 'withdraw' and account.balance < amount:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)

            if transaction_type == 'deposit':
                account.balance += amount
            else:  # withdrawal
                account.balance -= amount

            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)
            return JsonResponse({'message': 'Transaction successful', 'new_balance': account.balance}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
```