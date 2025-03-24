```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    transactions = Transaction.objects.filter(account=account).order_by('-date')

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.user = request.user
            transaction.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = TransactionForm()

    context = {
        'account': account,
        'transactions': transactions,
        'form': form,
    }
    return render(request, 'bank/account_detail.html', context)

@login_required
@csrf_exempt
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'account_id': account.id}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    form = AccountForm()
    return render(request, 'bank/create_account.html', {'form': form})
```