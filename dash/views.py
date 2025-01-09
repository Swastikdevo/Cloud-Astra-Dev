```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_overview', account_id=account.id)
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["POST"])
def transfer_funds(request):
    if request.is_ajax() and request.method == "POST":
        sender_account_id = request.POST.get('sender_account_id')
        receiver_account_id = request.POST.get('receiver_account_id')
        amount = request.POST.get('amount')

        sender_account = Account.objects.get(id=sender_account_id, user=request.user)
        receiver_account = Account.objects.get(id=receiver_account_id)

        if sender_account.balance >= float(amount):
            sender_account.balance -= float(amount)
            receiver_account.balance += float(amount)
            sender_account.save()
            receiver_account.save()

            transaction = Transaction(sender=sender_account, receiver=receiver_account, amount=amount)
            transaction.save()

            return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request!'})
```