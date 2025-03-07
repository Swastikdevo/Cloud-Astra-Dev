```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm

@login_required
@csrf_exempt
def bank_management_view(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_account':
            account_name = request.POST.get('account_name')
            Account.objects.create(owner=user, name=account_name)
            return JsonResponse({'message': 'Account created successfully.'})

        elif action == 'transfer_funds':
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account_id = form.cleaned_data['from_account']
                to_account_id = form.cleaned_data['to_account']
                amount = form.cleaned_data['amount']

                from_account = Account.objects.get(id=from_account_id, owner=user)
                to_account = Account.objects.get(id=to_account_id, owner=user)

                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    
                    Transaction.objects.create(
                        from_account=from_account,
                        to_account=to_account,
                        amount=amount
                    )
                    return JsonResponse({'message': 'Transfer successful.'})
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

    return render(request, 'bank_management.html', {'accounts': accounts})
```