```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'message': 'Account created successfully.', 'account_id': account.id}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'accounts': accounts})

@login_required
@require_http_methods(["GET", "POST"])
def make_transaction(request):
    if request.method == "POST":
        account_id = request.POST.get('account_id')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('type')

        try:
            account = Account.objects.get(id=account_id, user=request.user)
            if transaction_type == 'deposit':
                account.balance += float(amount)
            elif transaction_type == 'withdraw' and account.balance >= float(amount):
                account.balance -= float(amount)
            else:
                return JsonResponse({'error': 'Insufficient funds for withdrawal.'}, status=400)

            account.save()
            transaction = Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)
            return JsonResponse({'message': 'Transaction successful.', 'transaction_id': transaction.id}, status=201)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
```