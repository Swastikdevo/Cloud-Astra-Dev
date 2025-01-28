```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(user=request.user)
            transaction.save()
            return JsonResponse({'message': 'Transaction successful!', 'transaction_id': transaction.id})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    form = TransactionForm()
    
    return render(request, 'account_management.html', {
        'accounts': accounts,
        'transactions': transactions,
        'form': form
    })
```