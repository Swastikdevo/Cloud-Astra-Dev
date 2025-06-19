```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
def manage_bank_account(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Account created successfully!'}, status=201)
            else:
                return JsonResponse({'errors': form.errors}, status=400)

        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save()
                return JsonResponse({'message': 'Transaction successful!', 'transaction_id': transaction.id}, status=201)
            else:
                return JsonResponse({'errors': form.errors}, status=400)

    elif request.method == 'GET':
        accounts = Account.objects.all()
        transactions = Transaction.objects.all()
        return render(request, 'bank/manage_accounts.html', {'accounts': accounts, 'transactions': transactions})

    return JsonResponse({'message': 'Invalid request method.'}, status=405)
```