```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

class BankView(View):
    @login_required
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/dashboard.html', {'accounts': accounts})

    @login_required
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = Account.objects.get(id=form.cleaned_data['sender_account'])
                recipient_account = Account.objects.get(id=form.cleaned_data['recipient_account'])
                amount = form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(
                        account=sender_account,
                        amount=-amount,
                        transaction_type='Transfer',
                        description=f'Transferred to {recipient_account.account_number}'
                    )
                    Transaction.objects.create(
                        account=recipient_account,
                        amount=amount,
                        transaction_type='Transfer',
                        description=f'Received from {sender_account.account_number}'
                    )
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

        elif action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(id=form.cleaned_data['account'])
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Deposit',
                    description='Deposit'
                )
                return JsonResponse({'status': 'success', 'message': 'Deposit successful.'})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(id=form.cleaned_data['account'])
                amount = form.cleaned_data['amount']
                
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        amount=-amount,
                        transaction_type='Withdrawal',
                        description='Withdrawal'
                    )
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
```