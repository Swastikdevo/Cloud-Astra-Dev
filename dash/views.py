```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')
    form = TransferForm()

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            source_account = form.cleaned_data['source_account']
            target_account = form.cleaned_data['target_account']
            amount = form.cleaned_data['amount']
            if source_account.balance >= amount:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()
                
                Transaction.objects.create(account=source_account, amount=-amount)
                Transaction.objects.create(account=target_account, amount=amount)

                return JsonResponse({'success': True, 'message': 'Transfer successful'})
            else:
                return JsonResponse({'success': False, 'message': 'Insufficient funds'})

    context = {
        'accounts': user_accounts,
        'transactions': transactions,
        'form': form
    }
    return render(request, 'bank/account_dashboard.html', context)
```