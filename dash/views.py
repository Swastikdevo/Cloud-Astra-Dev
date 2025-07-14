```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, AccountForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@require_POST
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        sender_account = form.cleaned_data['sender_account']
        recipient_account = form.cleaned_data['recipient_account']
        amount = form.cleaned_data['amount']

        if sender_account.balance >= amount:
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()

            Transaction.objects.create(
                sender=sender_account,
                recipient=recipient_account,
                amount=amount
            )
            return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid form submission.'})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('account_overview')
    else:
        form = AccountForm()

    return render(request, 'bank/create_account.html', {'form': form})
```