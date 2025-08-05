```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_accounts(request):
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('manage_accounts')
    else:
        form = AccountCreationForm()
    
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_accounts.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["GET", "POST"])
def transfer_funds(request):
    if request.method == "POST":
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
                return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'}, status=400)
    else:
        form = TransferForm()
    
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'transfer_funds.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["GET"])
def account_summary(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'account_summary.html', {'accounts': accounts})
```