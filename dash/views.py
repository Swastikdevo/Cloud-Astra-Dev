```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        sender_account = Account.objects.get(id=form.cleaned_data['sender_account_id'], user=request.user)
        receiver_account = Account.objects.get(id=form.cleaned_data['receiver_account_id'])
        amount = form.cleaned_data['amount']

        if sender_account.balance >= amount:
            # Perform the transfer
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()

            # Create a transaction record
            Transaction.objects.create(
                sender=sender_account,
                receiver=receiver_account,
                amount=amount,
                description=form.cleaned_data['description']
            )
            return redirect('dashboard')
        else:
            return HttpResponse("Insufficient funds", status=400)
    
    return HttpResponse("Invalid form data", status=400)
```