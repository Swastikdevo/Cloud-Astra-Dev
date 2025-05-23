```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Assume we have a BankAccount model and a transaction service defined in services.py
from .models import BankAccount
from .services import perform_transaction

@csrf_exempt
@require_http_methods(["POST"])
def manage_account(request):
    try:
        data = json.loads(request.body)
        action = data.get("action")
        account_id = data.get("account_id")
        
        if action == "create":
            account_name = data.get("account_name")
            balance = data.get("initial_balance", 0)
            account = BankAccount.objects.create(name=account_name, balance=balance)
            return JsonResponse({"message": "Account created", "account_id": account.id}, status=201)

        elif action == "deposit":
            amount = data.get("amount")
            account = BankAccount.objects.get(id=account_id)
            account.balance += amount
            account.save()
            return JsonResponse({"message": "Deposit successful", "new_balance": account.balance})

        elif action == "withdraw":
            amount = data.get("amount")
            account = BankAccount.objects.get(id=account_id)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                return JsonResponse({"message": "Withdrawal successful", "new_balance": account.balance})
            else:
                return JsonResponse({"message": "Insufficient funds"}, status=400)

        elif action == "transaction":
            transaction_data = data.get("transaction_data")
            result = perform_transaction(transaction_data)
            return JsonResponse(result)

        else:
            return JsonResponse({"message": "Invalid action"}, status=400)

    except BankAccount.DoesNotExist:
        return JsonResponse({"message": "Account not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
```