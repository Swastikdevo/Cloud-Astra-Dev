```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Account
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def create_account(request):
    try:
        data = json.loads(request.body)
        account_type = data.get('account_type')
        initial_balance = data.get('initial_balance', 0)
        
        if account_type not in ['savings', 'checking']:
            return JsonResponse({'error': 'Invalid account type'}, status=400)

        user = request.user
        account = Account.objects.create(user=user, account_type=account_type, balance=initial_balance)
        
        return JsonResponse({'message': 'Account created successfully', 'account_id': account.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def deposit_funds(request, account_id):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')

        if amount <= 0:
            return JsonResponse({'error': 'Deposit amount must be greater than zero'}, status=400)

        account = Account.objects.get(id=account_id, user=request.user)
        account.balance += amount
        account.save()
        
        return JsonResponse({'message': 'Funds deposited successfully', 'new_balance': account.balance}, status=200)

    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["GET"])
def account_details(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        
        return JsonResponse({
            'account_id': account.id,
            'account_type': account.account_type,
            'balance': account.balance,
            'user': account.user.username
        }, status=200)

    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```