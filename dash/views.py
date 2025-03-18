```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
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
            return redirect('manage_account')
        else:
            return render(request, 'bank/manage_account.html', {'form': form})

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def transaction_history(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = Account.objects.get(id=request.POST.get('account_id'), user=request.user)
        transaction.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
```