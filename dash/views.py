```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from .models import Account, Transaction
from .forms import TransactionForm

@method_decorator(login_required, name='dispatch')
class BankView(View):
    
    def get(self, request):
        accounts = Account.objects.filter(owner=request.user)
        transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
        form = TransactionForm()
        return render(request, 'bank/home.html', {'accounts': accounts, 'transactions': transactions, 'form': form})

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.user = request.user

            # Adding features: logging withdrawal/deposit
            if transaction.transaction_type == 'withdrawal':
                if transaction.amount > transaction.account.balance:
                    messages.error(request, "Insufficient funds!")
                    return redirect('bank-home')
                transaction.account.balance -= transaction.amount
            elif transaction.transaction_type == 'deposit':
                transaction.account.balance += transaction.amount

            transaction.account.save()
            transaction.save()
            messages.success(request, "Transaction completed successfully.")
            return redirect('bank-home')
        else:
            messages.error(request, "Failed to process transaction. Please check your data.")
            return redirect('bank-home')
```