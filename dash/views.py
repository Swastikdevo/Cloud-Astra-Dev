```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account
from .forms import AccountForm, TransactionForm

@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        context = {
            'accounts': accounts,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm(),
        }
        return render(request, 'bank_management.html', context)
    
    elif request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('bank_management_view')
        
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(pk=form.cleaned_data['account_id'])
                account.balance += form.cleaned_data['amount']
                account.save()
                return JsonResponse({'status': 'success', 'balance': account.balance})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
```