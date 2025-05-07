```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Account

@csrf_exempt
@require_http_methods(["POST"])
def create_account(request):
    try:
        data = json.loads(request.body)
        account_number = data.get('account_number')
        account_holder_name = data.get('account_holder_name')
        initial_balance = data.get('initial_balance', 0)

        if not account_number or not account_holder_name:
            return JsonResponse({'error': 'Account number and holder name are required.'}, status=400)

        account = Account(
            account_number=account_number,
            account_holder_name=account_holder_name,
            balance=initial_balance
        )
        account.save()

        return JsonResponse({'message': 'Account created successfully!', 'account_id': account.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def deposit(request):
    try:
        data = json.loads(request.body)
        account_id = data.get('account_id')
        amount = data.get('amount')

        if not account_id or amount is None:
            return JsonResponse({'error': 'Account ID and amount are required.'}, status=400)

        account = Account.objects.get(id=account_id)
        account.balance += amount
        account.save()

        return JsonResponse({'message': 'Deposit successful!', 'new_balance': account.balance}, status=200)

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
        account_id = data.get('account_id')
        amount = data.get('amount')

        if not account_id or amount is None:
            return JsonResponse({'error': 'Account ID and amount are required.'}, status=400)

        account = Account.objects.get(id=account_id)
        
        if amount > account.balance:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)

        account.balance -= amount
        account.save()

        return JsonResponse({'message': 'Withdrawal successful!', 'new_balance': account.balance}, status=200)

    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def account_details(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        return JsonResponse({
            'account_number': account.account_number,
            'account_holder_name': account.account_holder_name,
            'balance': account.balance
        }, status=200)

    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```