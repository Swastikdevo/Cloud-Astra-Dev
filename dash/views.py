```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
from django.db import transaction

@login_required
@csrf_exempt
def transfer_funds(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            source_account = get_object_or_404(Account, id=form.cleaned_data['source_account_id'], owner=request.user)
            target_account = get_object_or_404(Account, id=form.cleaned_data['target_account_id'])
            amount = form.cleaned_data['amount']

            if source_account.balance >= amount:
                with transaction.atomic():
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    Transaction.objects.create(
                        source_account=source_account,
                        target_account=target_account,
                        amount=amount,
                        transaction_type='transfer'
                    )
                return JsonResponse({'success': True, 'message': 'Transfer successful!'})
            else:
                return JsonResponse({'success': False, 'message': 'Insufficient funds.'})
        
        return JsonResponse({'success': False, 'message': 'Invalid form submission.'})
    
    return render(request, 'bank/transfer.html', {'form': TransactionForm()})
```