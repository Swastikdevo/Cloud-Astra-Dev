```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:
            account = get_object_or_404(Account, id=account_id, owner=request.user)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        if account_id:
            account = get_object_or_404(Account, id=account_id, owner=request.user)
            form = AccountForm(instance=account)
        else:
            form = AccountForm()
    
    return render(request, 'bank/manage_account.html', {'form': form})

@login_required
@require_POST
def transfer_funds(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        sender_account = get_object_or_404(Account, id=form.cleaned_data['sender_account_id'], owner=request.user)
        receiver_account = get_object_or_404(Account, id=form.cleaned_data['receiver_account_id'])
        amount = form.cleaned_data['amount']
        
        if sender_account.balance >= amount:
            # Create transaction record
            Transaction.objects.create(
                sender=sender_account,
                receiver=receiver_account,
                amount=amount
            )
            # Update account balances
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()
            return JsonResponse({'status': 'success', 'message': 'Funds transferred successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid form'}, status=400)

@login_required
def account_list(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_list.html', {'accounts': accounts})
```