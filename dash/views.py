```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

class BankView(View):
    
    @login_required
    def get(self, request):
        accounts = Account.objects.filter(owner=request.user)
        return render(request, 'bank/dashboard.html', {'accounts': accounts})

    @login_required
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                self.process_transfer(form, request.user)
                return JsonResponse({'status': 'success', 'message': 'Transfer completed.'})
        
        elif action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                self.process_deposit(form, request.user)
                return JsonResponse({'status': 'success', 'message': 'Deposit completed.'})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                self.process_withdrawal(form, request.user)
                return JsonResponse({'status': 'success', 'message': 'Withdrawal completed.'})

        return JsonResponse({'status': 'error', 'message': 'Invalid action.'})

    def process_transfer(self, form, user):
        source_account = form.cleaned_data['source_account']
        target_account = form.cleaned_data['target_account']
        amount = form.cleaned_data['amount']
        
        if source_account.balance >= amount:
            source_account.balance -= amount
            target_account.balance += amount
            source_account.save()
            target_account.save()
            Transaction.objects.create(account=source_account, amount=-amount, transaction_type='Transfer')
            Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer')
        else:
            raise ValueError("Insufficient funds.")

    def process_deposit(self, form, user):
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')

    def process_withdrawal(self, form, user):
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
        else:
            raise ValueError("Insufficient funds.")
```