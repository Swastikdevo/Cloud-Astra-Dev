```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = form.cleaned_data['sender_account']
                receiver_account = form.cleaned_data['receiver_account']
                amount = form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    
                    Transaction.objects.create(
                        sender=sender_account,
                        receiver=receiver_account,
                        amount=amount,
                        user=request.user
                    )
                    
                    messages.success(request, 'Transfer successful!')
                    return redirect('manage_account')
                else:
                    messages.error(request, 'Insufficient balance!')
            else:
                messages.error(request, 'Invalid transfer details!')
        
        elif action == 'deposit':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount'))
            account = Account.objects.get(id=account_id)
            account.balance += amount
            account.save()
            messages.success(request, 'Deposit successful!')

        elif action == 'withdraw':
            account_id = request.POST.get('account_id')
            amount = float(request.POST.get('amount'))
            account = Account.objects.get(id=account_id)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                messages.success(request, 'Withdrawal successful!')
            else:
                messages.error(request, 'Insufficient balance!')

        return redirect('manage_account')
```