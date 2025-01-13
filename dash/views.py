```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransferForm
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_account')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["POST"])
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
            messages.success(request, 'Transfer successful!')
            return JsonResponse({'status': 'success'})
        else:
            messages.error(request, 'Insufficient funds!')
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'}, status=400)

    messages.error(request, 'Invalid transfer details!')
    return JsonResponse({'status': 'error', 'message': 'Invalid transfer details!'}, status=400)
```