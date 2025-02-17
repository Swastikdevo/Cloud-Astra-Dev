```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(owner=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        if 'create_account' in request.POST:
            account_name = request.POST.get('account_name')
            new_account = Account.objects.create(owner=request.user, name=account_name, balance=0)
            return redirect('manage_account')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = Account.objects.get(id=form.cleaned_data['sender_account_id'], owner=request.user)
                recipient_account = Account.objects.get(id=form.cleaned_data['recipient_account_id'])
                amount = form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    
                    Transaction.objects.create(sender=sender_account, recipient=recipient_account, amount=amount)
                    return JsonResponse({'status': 'success', 'message': 'Transfer completed.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
```