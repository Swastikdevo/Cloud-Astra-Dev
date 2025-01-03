```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_summary(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
    
    if request.method == 'POST':
        # Handle deposit or withdrawal
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_summary')
                
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    return redirect('account_summary')
                else:
                    error_message = 'Insufficient funds.'
    
    else:
        form = DepositForm()

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': form,
        'withdraw_form': WithdrawForm(),
        'error_message': error_message if 'error_message' in locals() else None,
    }
    
    return render(request, 'account_summary.html', context)

@csrf_exempt
@login_required
def api_transaction_history(request):
    if request.method == 'GET':
        account = Account.objects.get(user=request.user)
        transactions = list(Transaction.objects.filter(account=account).values('date', 'amount', 'transaction_type'))
        return JsonResponse(transactions, safe=False)
```