```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import CreateAccountForm, DepositForm, WithdrawForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_account':
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('account_details', account_id=account.id)

        elif action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=request.POST.get('account_id'))
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'new_balance': account.balance})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=request.POST.get('account_id'))
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return JsonResponse({'success': True, 'new_balance': account.balance})
                else:
                    return JsonResponse({'success': False, 'error': 'Insufficient funds.'})

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'accounts': accounts})
```