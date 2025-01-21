```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank_management.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_account':
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully'}, status=201)
            return JsonResponse({'status': 'error', 'message': 'Failed to create account.'}, status=400)

        elif action == 'make_transaction':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction made successfully'}, status=201)
            return JsonResponse({'status': 'error', 'message': 'Failed to make transaction.'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
```