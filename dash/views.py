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
    template_name = 'bank_management.html'

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')[:10]  # Latest 10 transactions
        form = TransactionForm()
        return render(request, self.template_name, {'accounts': accounts, 'transactions': transactions, 'form': form})

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction recorded successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data!'}, status=400)

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('bank_management')
    else:
        form = AccountForm()
    return render(request, 'create_account.html', {'form': form})
```