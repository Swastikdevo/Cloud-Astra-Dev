```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import CreateAccountForm, TransferForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Handle account creation
        if action == 'create_account':
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': form.errors})

        # Handle money transfer
        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = Account.objects.get(id=form.cleaned_data['sender_account_id'])
                receiver_account = Account.objects.get(id=form.cleaned_data['receiver_account_id'])
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
                        description=f'Transferred {amount} to {receiver_account.account_number}'
                    )
                    return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
            else:
                return JsonResponse({'status': 'error', 'message': form.errors})

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank_management.html', {'accounts': accounts})
```