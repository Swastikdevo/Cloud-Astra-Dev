```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
import json

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'accounts/manage.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create':
            account_name = data.get('account_name')
            new_account = Account.objects.create(user=request.user, name=account_name)
            return JsonResponse({'status': 'success', 'account_id': new_account.id})

        elif action == 'update':
            account_id = data.get('account_id')
            new_name = data.get('account_name')
            try:
                account = Account.objects.get(id=account_id, user=request.user)
                account.name = new_name
                account.save()
                return JsonResponse({'status': 'success', 'account_id': account.id})
            except Account.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)

        elif action == 'delete':
            account_id = data.get('account_id')
            try:
                account = Account.objects.get(id=account_id, user=request.user)
                account.delete()
                return JsonResponse({'status': 'success', 'message': 'Account deleted'})
            except Account.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
```