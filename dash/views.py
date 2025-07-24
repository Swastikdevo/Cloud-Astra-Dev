```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Associate transaction with the logged-in user
            transaction.save()

            # Optionally handle account balance updates
            account = Account.objects.get(id=transaction.account.id)
            if transaction.transaction_type == 'deposit':
                account.balance += transaction.amount
            elif transaction.transaction_type == 'withdrawal':
                account.balance -= transaction.amount
            account.save()

            return redirect('transaction_success')  # Redirect to a success page or list of transactions
    else:
        form = TransactionForm()

    return render(request, 'bank/create_transaction.html', {'form': form})

@login_required
@require_http_methods(["GET"])
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/view_transactions.html', {'transactions': transactions})
```