```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import TransactionForm

@method_decorator(login_required, name='dispatch')
def account_summary(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_summary.html', {'accounts': accounts})

@csrf_exempt
@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction created successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid transaction data.'}, status=400)
    return render(request, 'bank/create_transaction.html', {'form': TransactionForm()})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

@login_required
def delete_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        transaction.delete()
        return redirect('transaction_history')
    except Transaction.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Transaction not found.'}, status=404)
```