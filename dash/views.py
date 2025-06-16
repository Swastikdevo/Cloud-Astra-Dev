```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.db import transaction

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'create':
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': form.errors})

        elif request.POST.get('action') == 'deposit':
            form = TransactionForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
                    account.balance += form.cleaned_data['amount']
                    account.save()
                    Transaction.objects.create(account=account, amount=form.cleaned_data['amount'], type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful.'})
            else:
                return JsonResponse({'status': 'error', 'message': form.errors})

        elif request.POST.get('action') == 'withdraw':
            form = TransactionForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
                    if account.balance >= form.cleaned_data['amount']:
                        account.balance -= form.cleaned_data['amount']
                        account.save()
                        Transaction.objects.create(account=account, amount=form.cleaned_data['amount'], type='withdraw')
                        return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'accounts': accounts})
```