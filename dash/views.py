```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@method_decorator(login_required, name='dispatch')
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return JsonResponse({'status': 'success', 'account_id': new_account.id})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'accounts': accounts})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        return JsonResponse({'status': 'error', 'errors': form.errors})

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/make_transaction.html', {'accounts': accounts})
```