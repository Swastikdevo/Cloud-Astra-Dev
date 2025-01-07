```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["POST"])
def transfer_funds(request):
    if request.is_ajax():
        from_account_id = request.POST.get('from_account_id')
        to_account_id = request.POST.get('to_account_id')
        amount = request.POST.get('amount')

        from_account = Account.objects.get(id=from_account_id, user=request.user)
        to_account = Account.objects.get(id=to_account_id)

        if from_account.balance >= float(amount):
            from_account.balance -= float(amount)
            to_account.balance += float(amount)
            from_account.save()
            to_account.save()

            transaction = Transaction.objects.create(
                from_account=from_account,
                to_account=to_account,
                amount=amount
            )

            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
@require_http_methods(["GET"])
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(from_account=account)
    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})
```