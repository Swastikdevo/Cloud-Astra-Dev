```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
import json

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        action_type = data.get('action')

        if action_type == 'create':
            form = AccountForm(data)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})

        elif action_type == 'update':
            account_id = data.get('account_id')
            account = Account.objects.get(id=account_id, user=request.user)
            form = AccountForm(data, instance=account)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Account updated successfully!'})
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})

        elif action_type == 'delete':
            account_id = data.get('account_id')
            Account.objects.filter(id=account_id, user=request.user).delete()
            return JsonResponse({'status': 'success', 'message': 'Account deleted successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Unsupported method'})
```