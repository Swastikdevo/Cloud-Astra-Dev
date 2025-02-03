```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/dashboard.html', {'accounts': accounts})

    def post(self, request):
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'message': 'Deposit successful!'})
                
        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
                    return JsonResponse({'message': 'Withdrawal successful!'})
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
        
        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
                amount = form.cleaned_data['amount']
                if from_account.balance >= amount:
                    Transaction.objects.create(account=from_account, amount=-amount, transaction_type='Transfer')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer')
                    return JsonResponse({'message': 'Transfer successful!'})
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

        return JsonResponse({'error': 'Invalid action'}, status=400)
```