```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': user_accounts})

@method_decorator(login_required, name='dispatch')
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            sender_account = form.cleaned_data['sender_account']
            receiver_account = form.cleaned_data['receiver_account']
            
            if sender_account.balance >= amount:
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()
                
                Transaction.objects.create(
                    sender=sender_account,
                    receiver=receiver_account,
                    amount=amount,
                )
                
                return redirect('account_overview')
            else:
                form.add_error('amount', 'Insufficient funds.')
    else:
        form = TransferForm()
    
    return render(request, 'bank/transfer_funds.html', {'form': form})

@login_required
@require_POST
def check_balance(request):
    account_id = request.POST.get('account_id')
    account = Account.objects.get(pk=account_id)
    
    return JsonResponse({'balance': account.balance})
```