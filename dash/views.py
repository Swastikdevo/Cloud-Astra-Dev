```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import TransactionForm
from django.utils import timezone

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.date = timezone.now()
            transaction.save()
            return JsonResponse({'message': 'Transaction completed successfully!', 'transaction_id': transaction.id}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    context = {
        'accounts': accounts,
        'transactions': transactions,
        'form': TransactionForm(),
    }
    return render(request, 'bank/manage_account.html', context)
```