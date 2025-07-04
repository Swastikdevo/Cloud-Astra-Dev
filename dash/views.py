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
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({"status": "success", "message": "Account created successfully!"}, status=201)
        
        elif 'deposit' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.type = 'deposit'
                transaction.save()
                account = Account.objects.get(id=request.POST['account_id'])
                account.balance += transaction.amount
                account.save()
                return JsonResponse({"status": "success", "message": "Deposit successful!", "new_balance": account.balance})

        elif 'withdraw' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.type = 'withdraw'
                account = Account.objects.get(id=request.POST['account_id'])

                if account.balance >= transaction.amount:
                    transaction.save()
                    account.balance -= transaction.amount
                    account.save()
                    return JsonResponse({"status": "success", "message": "Withdrawal successful!", "new_balance": account.balance})
                else:
                    return JsonResponse({"status": "error", "message": "Insufficient funds!"}, status=400)

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'accounts': accounts})
```