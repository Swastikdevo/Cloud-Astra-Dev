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
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountCreationForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.owner = request.user
                account.save()
                return redirect('account_detail', account.id)

        elif 'transfer_funds' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender_account = Account.objects.get(id=transfer_form.cleaned_data['sender_account'])
                receiver_account = Account.objects.get(id=transfer_form.cleaned_data['receiver_account'])
                
                amount = transfer_form.cleaned_data['amount']
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
                    return JsonResponse({'success': True, 'message': 'Transfer successful.'})
                else:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds.'})

    accounts = Account.objects.filter(owner=request.user)
    transfer_form = TransferForm()
    account_creation_form = AccountCreationForm()
    
    return render(request, 'manage_account.html', {
        'accounts': accounts,
        'transfer_form': transfer_form,
        'account_creation_form': account_creation_form,
    })
```