```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def manage_account(request, account_id=None):
    if request.method == "GET":
        if account_id:
            account = get_object_or_404(Account, id=account_id)
            return render(request, 'account_detail.html', {'account': account})
        else:
            accounts = Account.objects.filter(user=request.user)
            return render(request, 'account_list.html', {'accounts': accounts})

    elif request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('manage_account')
    
    elif request.method == "DELETE" and account_id:
        account = get_object_or_404(Account, id=account_id, user=request.user)
        account.delete()
        return JsonResponse({'success': True}, status=204)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def record_transaction(request, account_id):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = get_object_or_404(Account, id=account_id, user=request.user)
            transaction.save()
            return JsonResponse({'success': True, 'transaction_id': transaction.id}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)
```