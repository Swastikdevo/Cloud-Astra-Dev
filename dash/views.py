```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import TransferForm, AccountCreationForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.owner = request.user
            new_account.save()
            return redirect('account_overview')
    else:
        form = AccountCreationForm()

    accounts = Account.objects.filter(owner=request.user)

    return render(request, 'bank/manage_account.html', {
        'form': form,
        'accounts': accounts,
    })

@login_required
@require_http_methods(["POST"])
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        source_account = form.cleaned_data['source_account']
        destination_account = form.cleaned_data['destination_account']
        amount = form.cleaned_data['amount']

        if source_account.balance >= amount:
            source_account.balance -= amount
            destination_account.balance += amount
            source_account.save()
            destination_account.save()

            Transaction.objects.create(
                source_account=source_account,
                destination_account=destination_account,
                amount=amount,
                user=request.user
            )
            return JsonResponse({'status': 'success', 'message': 'Transfer successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    return JsonResponse({'status': 'error', 'message': 'Invalid form data'})
```