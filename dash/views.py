```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'accounts': accounts, 'form': AccountForm()})

@login_required
@require_http_methods(["GET", "POST"])
@csrf_exempt
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'message': 'Transaction completed successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'bank/make_transaction.html', {'transactions': transactions, 'form': TransactionForm()})
```