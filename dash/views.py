```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@csrf_exempt
def account_summary(request):
    user = request.user
    account = Account.objects.filter(owner=user).first()
    
    if account is None:
        return JsonResponse({'error': 'No account found for this user.'}, status=404)

    if request.method == 'GET':
        transactions = Transaction.objects.filter(account=account).order_by('-date')
        return render(request, 'bank/account_summary.html', {
            'account': account,
            'transactions': transactions
        })

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'message': 'Transaction successfully recorded!'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
```