```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account
from .forms import AccountForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    context = {
        'form': form,
        'accounts': accounts,
    }
    return render(request, 'bank/manage_account.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def deposit_funds(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount.isdigit() and float(amount) > 0:
            account.balance += float(amount)
            account.save()
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid amount'})

    return render(request, 'bank/deposit_funds.html', {'account': account})

@login_required
@require_http_methods(["POST"])
def withdraw_funds(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    amount = request.POST.get('amount')
    if amount.isdigit() and float(amount) > 0 and account.balance >= float(amount):
        account.balance -= float(amount)
        account.save()
        return JsonResponse({'status': 'success', 'new_balance': account.balance})

    return JsonResponse({'status': 'error', 'message': 'Insufficient funds or invalid amount'})

@login_required
@require_http_methods(["POST"])
def transfer_funds(request, account_id):
    source_account = Account.objects.get(id=account_id, user=request.user)
    target_account_id = request.POST.get('target_account_id')
    amount = request.POST.get('amount')
    
    if amount.isdigit() and float(amount) > 0:
        target_account = Account.objects.get(id=target_account_id, user=request.user)
        if source_account.balance >= float(amount):
            source_account.balance -= float(amount)
            target_account.balance += float(amount)
            source_account.save()
            target_account.save()
            return JsonResponse({'status': 'success', 'new_source_balance': source_account.balance, 'new_target_balance': target_account.balance})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    return JsonResponse({'status': 'error', 'message': 'Invalid amount'})
```