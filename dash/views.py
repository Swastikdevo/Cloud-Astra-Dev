```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(owner=request.user)
        return render(request, 'bank_management/dashboard.html', {'accounts': accounts})

    elif request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.owner = request.user
                account.save()
                return redirect('bank_management')

        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = get_object_or_404(Account, id=request.POST['account_id'], owner=request.user)
                transaction.save()
                return redirect('bank_management')

    return JsonResponse({'error': 'Invalid request'}, status=400)
```