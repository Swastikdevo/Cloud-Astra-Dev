```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_management')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'account_management.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["POST"])
def make_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = request.user.account
        transaction.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    return JsonResponse({'status': 'fail', 'errors': form.errors})

@login_required
@require_http_methods(["GET"])
def transaction_history(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    return render(request, 'transaction_history.html', {'transactions': transactions})
```