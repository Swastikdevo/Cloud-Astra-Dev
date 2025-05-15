```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
        transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
        context = {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm(),
        }
        return render(request, self.template_name, context)

    @csrf_exempt
    def post(self, request):
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                account = account_form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('bank_management')

        elif 'create_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.account = Account.objects.get(id=request.POST['account_id'])
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction saved!'}, status=200)

        return redirect('bank_management')
```