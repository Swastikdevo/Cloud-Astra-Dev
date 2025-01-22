```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

from .models import Account, Transaction
from .utils import generate_transaction_id

@csrf_exempt
@login_required
@require_POST
def create_transaction(request):
    try:
        data = json.loads(request.body)
        account_id = data.get('account_id')
        transaction_type = data.get('transaction_type')
        amount = data.get('amount')

        # Validate input
        if account_id is None or transaction_type not in ['deposit', 'withdraw'] or amount <= 0:
            return JsonResponse({'error': 'Invalid input'}, status=400)

        # Fetch account
        account = Account.objects.get(id=account_id, user=request.user)
        
        if transaction_type == 'withdraw' and account.balance < amount:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)

        # Create transaction
        transaction_id = generate_transaction_id()
        transaction = Transaction.objects.create(
            transaction_id=transaction_id,
            account=account,
            amount=amount,
            transaction_type=transaction_type
        )

        # Update account balance
        if transaction_type == 'deposit':
            account.balance += amount
        else:  # withdraw
            account.balance -= amount
        account.save()

        return JsonResponse({
            'transaction_id': transaction.transaction_id,
            'new_balance': account.balance
        }, status=201)

    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```