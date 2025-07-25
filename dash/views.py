```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required, name='dispatch')
class BankManagementView(View):
    template_name = 'bank/manage.html'

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        transaction_form = TransactionForm()
        return render(request, self.template_name, {
            'accounts': accounts,
            'transaction_form': transaction_form,
        })

    def post(self, request):
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'success': True, 'message': 'Transaction recorded successfully!'})
        return JsonResponse({'success': False, 'errors': transaction_form.errors})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('bank:manage')
    else:
        form = AccountForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def account_details(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/account_details.html', {
        'account': account,
        'transactions': transactions,
    })
```