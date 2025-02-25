```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm
from django.db import transaction

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return redirect('bank:dashboard')
    else:
        form = AccountCreationForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def transfer_funds(request, account_id):
    sender_account = get_object_or_404(Account, id=account_id, owner=request.user)
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_account_id = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']
            
            with transaction.atomic():
                recipient_account = get_object_or_404(Account, id=recipient_account_id)
                
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()

                    Transaction.objects.create(
                        sender=sender_account,
                        recipient=recipient_account,
                        amount=amount
                    )
                    return JsonResponse({'success': True, 'message': 'Transfer successful.'})
                else:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds.'})
                
    else:
        form = TransferForm()
    return render(request, 'bank/transfer_funds.html', {'form': form, 'sender_account': sender_account})
```