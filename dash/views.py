```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

# Assuming there's a BankAccount model with balance and account_number
from .models import BankAccount

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def transfer_funds(request):
    data = json.loads(request.body)
    
    from_account_number = data.get('from_account_number')
    to_account_number = data.get('to_account_number')
    amount = data.get('amount')

    try:
        from_account = BankAccount.objects.get(account_number=from_account_number)
        to_account = BankAccount.objects.get(account_number=to_account_number)

        if from_account.balance < amount:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)

        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()

        return JsonResponse({'success': 'Transfer completed', 'new_balance': from_account.balance}, status=200)

    except BankAccount.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```