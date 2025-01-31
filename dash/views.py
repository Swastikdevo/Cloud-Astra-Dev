```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import TransferForm
from django.contrib.auth.decorators import login_required
from django.db import transaction

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
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
                        )
                        return JsonResponse({'status': 'success', 'message': 'Transfer successful!'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank_management.html', {'accounts': accounts})
```