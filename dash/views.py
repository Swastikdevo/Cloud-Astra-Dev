```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is not valid.'}, status=400)
    else:
        accounts = Account.objects.filter(owner=request.user)
        form = TransactionForm()
    
    return render(request, 'transaction.html', {
        'form': form,
        'accounts': accounts,
    })

@login_required
@require_http_methods(["GET"])
def transaction_history_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transaction_history.html', {
        'transactions': transactions,
    })
```