```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def transfer_funds(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            source_account = form.cleaned_data['source_account']
            target_account = form.cleaned_data['target_account']
            amount = form.cleaned_data['amount']

            try:
                source = Account.objects.get(id=source_account.id, owner=request.user)
                target = Account.objects.get(id=target_account.id)

                if source.balance >= amount:
                    # Deduct from source account and add to target account
                    source.balance -= amount
                    target.balance += amount
                    source.save()
                    target.save()

                    # Log the transaction
                    Transaction.objects.create(
                        source_account=source,
                        target_account=target,
                        amount=amount,
                        user=request.user
                    )

                    return redirect('transfer_success')
                else:
                    return render(request, 'transfer_funds.html', {
                        'form': form,
                        'error': 'Insufficient funds in the source account.'
                    })

            except Account.DoesNotExist:
                return render(request, 'transfer_funds.html', {
                    'form': form,
                    'error': 'Source or target account does not exist.'
                })

    else:
        form = TransactionForm()

    return render(request, 'transfer_funds.html', {
        'form': form
    })
```