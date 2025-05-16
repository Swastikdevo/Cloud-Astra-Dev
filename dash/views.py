```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({"message": "Transaction successful!", "transaction_id": transaction.id}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'accounts': accounts, 'form': TransactionForm()})

@login_required
@require_http_methods(["GET"])
def view_transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```