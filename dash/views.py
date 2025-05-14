```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = get_object_or_404(Account, id=form.cleaned_data['account_id'], user=request.user)

            # Implementing new features: transaction type (deposit/withdrawal)
            transaction_type = form.cleaned_data['transaction_type']
            if transaction_type == 'deposit':
                account.balance += amount
            elif transaction_type == 'withdrawal':
                if amount > account.balance:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)
                account.balance -= amount
            else:
                return JsonResponse({'error': 'Invalid transaction type.'}, status=400)

            account.save()
            transaction = Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type=transaction_type
            )
            return JsonResponse({'success': 'Transaction completed.', 'transaction_id': transaction.id})

    else:
        form = TransactionForm()

    return render(request, 'bank/transaction.html', {'form': form})
```