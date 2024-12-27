```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')[:10]
    
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.save()
            return redirect('bank_dashboard')
    else:
        form = TransactionForm()

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'form': form,
    }
    
    return render(request, 'bank/dashboard.html', context)

@login_required
def transfer_funds(request):
    if request.method == "POST":
        source_account = Account.objects.get(id=request.POST['source_account'])
        target_account = Account.objects.get(id=request.POST['target_account'])
        amount = float(request.POST['amount'])
        
        if source_account.balance >= amount:
            source_account.balance -= amount
            target_account.balance += amount
            source_account.save()
            target_account.save()
            Transaction.objects.create(account=source_account, amount=-amount, transaction_type='transfer', target_account=target_account)
            Transaction.objects.create(account=target_account, amount=amount, transaction_type='transfer', source_account=source_account)
            return JsonResponse({'status': 'success', 'message': 'Funds transferred successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/transfer.html', {'accounts': accounts})
```