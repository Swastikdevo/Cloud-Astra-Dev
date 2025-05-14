```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferFundsForm, AccountCreationForm

@login_required
@require_http_methods(["GET", "POST"])
def bank_management_view(request):
    if request.method == "POST":
        # Handle fund transfer
        transfer_form = TransferFundsForm(request.POST)
        if transfer_form.is_valid():
            from_account = transfer_form.cleaned_data['from_account']
            to_account = transfer_form.cleaned_data['to_account']
            amount = transfer_form.cleaned_data['amount']

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
                return JsonResponse({'status': 'success', 'message': 'Transfer successful'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    else:
        transfer_form = TransferFundsForm()
    
    # Account creation
    if request.GET.get('new_account', None) == 'true':
        account_creation_form = AccountCreationForm(request.GET)
        if account_creation_form.is_valid():
            new_account = account_creation_form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully'})

    context = {
        'transfer_form': transfer_form,
        'accounts': Account.objects.filter(user=request.user),
    }
    return render(request, 'bank_management.html', context)
```