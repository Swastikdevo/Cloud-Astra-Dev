```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_dashboard(request):
    account = BankAccount.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    # Process any forms submitted
    if request.method == 'POST':
        if 'deposit' in request.POST:
            return handle_deposit(request, account)
        elif 'withdraw' in request.POST:
            return handle_withdrawal(request, account)

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    return render(request, 'bank/account_dashboard.html', context)

@require_POST
@login_required
def handle_deposit(request, account):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return redirect('account_dashboard')

    return JsonResponse({'error': form.errors}, status=400)

@require_POST
@login_required
def handle_withdrawal(request, account):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount <= account.balance:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return redirect('account_dashboard')
        else:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)

    return JsonResponse({'error': form.errors}, status=400)
```