```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
import json

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
@require_http_methods(["POST", "GET"])
def bank_management_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")

        if action == "create_account":
            account_type = data.get("account_type")
            balance = data.get("balance", 0)
            account = Account.objects.create(owner=request.user, account_type=account_type, balance=balance)
            return JsonResponse({"message": "Account created successfully", "account_id": account.id}, status=201)

        elif action == "make_transaction":
            account_id = data.get("account_id")
            amount = data.get("amount")
            transaction_type = data.get("transaction_type")

            account = Account.objects.get(id=account_id, owner=request.user)

            if transaction_type == "deposit":
                account.balance += amount
                Transaction.objects.create(account=account, amount=amount, transaction_type="deposit")
                account.save()
                return JsonResponse({"message": "Deposit successful", "new_balance": account.balance})

            elif transaction_type == "withdraw":
                if account.balance >= amount:
                    account.balance -= amount
                    Transaction.objects.create(account=account, amount=amount, transaction_type="withdraw")
                    account.save()
                    return JsonResponse({"message": "Withdrawal successful", "new_balance": account.balance})
                else:
                    return JsonResponse({"error": "Insufficient balance"}, status=400)

    elif request.method == "GET":
        accounts = Account.objects.filter(owner=request.user).values("id", "account_type", "balance")
        return JsonResponse({"accounts": list(accounts)}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)
```