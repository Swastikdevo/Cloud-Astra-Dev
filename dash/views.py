```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            return JsonResponse({'status': 'success', 'account_id': account.id}, status=201)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    accounts = Account.objects.all()
    return render(request, 'management/manage_account.html', {'accounts': accounts})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def make_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=201)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return render(request, 'management/make_transaction.html')
```