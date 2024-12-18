```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = get_object_or_404(Account, user=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'balance': account.balance})
                
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return JsonResponse({'status': 'success', 'balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'}, status=400)
    
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    }
    
    return render(request, 'bank/manage_account.html', context)
```