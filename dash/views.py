```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Account, Transaction
import json

@csrf_exempt
@login_required
@require_http_methods(['POST'])
def create_transaction(request):
    data = json.loads(request.body)
    account_id = data.get('account_id')
    transaction_type = data.get('transaction_type')  # "deposit" or "withdrawal"
    amount = data.get('amount')

    if not account_id or not transaction_type or amount is None:
        return JsonResponse({"error": "Missing required fields."}, status=400)

    account = get_object_or_404(Account, id=account_id)

    if transaction_type not in ['deposit', 'withdrawal']:
        return JsonResponse({"error": "Invalid transaction type."}, status=400)

    if transaction_type == 'withdrawal' and account.balance < amount:
        return JsonResponse({"error": "Insufficient funds."}, status=400)

    # Process transaction
    if transaction_type == 'deposit':
        account.balance += amount
    else:  # withdrawal
        account.balance -= amount

    account.save()

    # Create a transaction record
    Transaction.objects.create(account=account, type=transaction_type, amount=amount)

    return JsonResponse({"message": "Transaction successful.", "new_balance": account.balance}, status=201)
```