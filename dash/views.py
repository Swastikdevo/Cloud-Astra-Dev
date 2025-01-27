```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Account, Transaction
from .forms import AccountForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'success': True, 'message': 'Account created successfully!'})
            return JsonResponse({'success': False, 'errors': form.errors})
        
        elif action == 'delete':
            account_id = request.POST.get('account_id')
            try:
                account = Account.objects.get(pk=account_id, user=request.user)
                account.delete()
                return JsonResponse({'success': True, 'message': 'Account deleted successfully!'})
            except Account.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Account not found.'})
        
        elif action == 'update':
            account_id = request.POST.get('account_id')
            account = Account.objects.get(pk=account_id)
            if account.user != request.user:
                raise PermissionDenied
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Account updated successfully!'})
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
```