```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

@method_decorator(login_required, name='dispatch')
@csrf_exempt
def transaction_history(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(account__user=request.user)
        return render(request, 'bank/transaction_history.html', {'transactions': transactions})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.save()
            return JsonResponse({'message': 'Transaction recorded successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

@login_required
def delete_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        account.delete()
        return JsonResponse({'message': 'Account deleted successfully!'}, status=204)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found.'}, status=404)
```