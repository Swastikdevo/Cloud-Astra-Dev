```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@require_GET
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': user_accounts})

@login_required
@require_POST
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        if account.owner == request.user:
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'success': True, 'message': 'Deposit successful!'})
        else:
            return JsonResponse({'success': False, 'message': 'Unauthorized access!'})
    return JsonResponse({'success': False, 'message': 'Invalid form submission.'})

@login_required
@require_POST
def withdrawal(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        if account.owner == request.user and account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
            return JsonResponse({'success': True, 'message': 'Withdrawal successful!'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient funds or unauthorized access!'})
    return JsonResponse({'success': False, 'message': 'Invalid form submission.'})

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        from_account = form.cleaned_data['from_account']
        to_account = form.cleaned_data['to_account']
        amount = form.cleaned_data['amount']
        if from_account.owner == request.user and from_account.balance >= amount and to_account.owner != request.user:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, amount=-amount, transaction_type='transfer')
            Transaction.objects.create(account=to_account, amount=amount, transaction_type='transfer')
            return JsonResponse({'success': True, 'message': 'Transfer successful!'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient funds or unauthorized access!'})
    return JsonResponse({'success': False, 'message': 'Invalid form submission.'})
```