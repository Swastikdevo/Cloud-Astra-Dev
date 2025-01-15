```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({"status": "success", "message": "Transaction completed successfully!"})
        return JsonResponse({"status": "error", "message": "Invalid transaction data."})

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    form = TransactionForm()

    return render(request, 'bank/manage_account.html', {
        'accounts': accounts,
        'transactions': transactions,
        'form': form,
    })
```