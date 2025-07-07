```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts)
        return render(request, 'bank_management.html', {'accounts': accounts, 'transactions': transactions})
    
    elif request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('bank_management')  # Redirect to the same view to display updated info
        
        elif 'new_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = form.cleaned_data['account']
                transaction.save()
                return redirect('bank_management')  # Redirect to the view after transaction
        
        elif 'ajax_balance' in request.POST:
            account_id = request.POST.get('account_id')
            account = Account.objects.get(id=account_id, user=request.user)
            return JsonResponse({'balance': account.balance})

    return render(request, 'bank_management.html')
```