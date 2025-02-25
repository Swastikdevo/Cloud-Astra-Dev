```python
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):
    template_name = 'bank_management.html'

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')[:10]
        account_form = AccountForm()
        transaction_form = TransactionForm()
        context = {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': account_form,
            'transaction_form': transaction_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                new_account = account_form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                return redirect('bank_management')

        elif 'create_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction_form.save()
                return redirect('bank_management')

        return redirect('bank_management')
```