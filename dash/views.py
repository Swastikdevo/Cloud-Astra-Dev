```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        action = request.POST.get("action")
        user_account = Account.objects.get(user=request.user)

        if action == "deposit":
            amount = float(request.POST.get("amount"))
            if amount > 0:
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='deposit')
                messages.success(request, "Deposit successful!")
            else:
                messages.error(request, "Invalid deposit amount.")

        elif action == "withdraw":
            amount = float(request.POST.get("amount"))
            if 0 < amount <= user_account.balance:
                user_account.balance -= amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='withdraw')
                messages.success(request, "Withdrawal successful!")
            else:
                messages.error(request, "Invalid withdrawal amount or insufficient funds.")

        elif action == "view_balance":
            return JsonResponse({"balance": user_account.balance})

        return redirect('manage_account')

    transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')
    return render(request, "bank/manage_account.html", {"transactions": transactions})
```