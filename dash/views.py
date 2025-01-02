```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
import json

@csrf_exempt
@require_http_methods(["POST"])
def create_account(request):
    try:
        data = json.loads(request.body)
        account_number = data.get('account_number')
        account_holder = data.get('account_holder')
        initial_balance = data.get('initial_balance', 0)

        if Account.objects.filter(account_number=account_number).exists():
            return JsonResponse({'error': 'Account already exists'}, status=400)

        new_account = Account.objects.create(
            account_number=account_number,
            account_holder=account_holder,
            balance=initial_balance
        )
        return JsonResponse({'message': 'Account created successfully', 'account_number': new_account.account_number}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def deposit(request):
    try:
        data = json.loads(request.body)
        account_number = data.get('account_number')
        amount = data.get('amount')

        account = Account.objects.get(account_number=account_number)
        account.balance += amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type='deposit',
            amount=amount
        )

        return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance}, status=200)

    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def withdraw(request):
    try:
        data = json.loads(request.body)
        account_number = data.get('account_number')
        amount = data.get('amount')

        account = Account.objects.get(account_number=account_number)

        if account.balance < amount:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)

        account.balance -= amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type='withdrawal',
            amount=amount
        )

        return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance}, status=200)

    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```