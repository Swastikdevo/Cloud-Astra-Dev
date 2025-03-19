```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = form.cleaned_data['sender_account']
            recipient_account = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()

                Transaction.objects.create(
                    sender=sender_account,
                    recipient=recipient_account,
                    amount=amount,
                    user=request.user
                )
                return JsonResponse({'status': 'success', 'message': 'Transfer successful.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'})

    else:
        form = TransferForm()
    
    return render(request, 'bank/transfer_funds.html', {'form': form})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_dashboard')

    else:
        form = AccountCreationForm()
    
    return render(request, 'bank/create_account.html', {'form': form})
```