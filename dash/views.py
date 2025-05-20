```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts)
        return render(request, 'bank_management/dashboard.html', {
            'accounts': accounts,
            'transactions': transactions,
        })

    def post(self, request):
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                messages.success(request, 'Account created successfully!')
                return redirect('bank_management')
        elif 'create_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Transaction recorded successfully!')
                return redirect('bank_management')
        messages.error(request, 'There was an error with your submission.')
        return redirect('bank_management')
```