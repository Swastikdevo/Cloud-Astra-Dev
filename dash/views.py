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
            return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form submission is invalid.'})

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date_created')
    form = TransactionForm()

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'form': form,
    }
    
    return render(request, 'bank/manage_account.html', context)
```