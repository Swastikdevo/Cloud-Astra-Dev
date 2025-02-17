```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        if 'create_account' in request.POST:
            form = AccountCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('account_overview')
        elif 'transfer_money' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender = request.user.account
                receiver_account = transfer_form.cleaned_data['receiver_account']
                amount = transfer_form.cleaned_data['amount']
                # Check sufficient balance
                if sender.balance >= amount:
                    Transaction.objects.create(sender=sender, receiver=receiver_account, amount=amount)
                    sender.balance -= amount
                    sender.save()
                    receiver_account.balance += amount
                    receiver_account.save()
                    return JsonResponse({'status': 'success', 'message': 'Transfer completed.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'}, status=400)
    else:
        transfer_form = TransferForm()
        creation_form = AccountCreationForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {
        'transfer_form': transfer_form,
        'creation_form': creation_form,
        'accounts': accounts,
    })
```