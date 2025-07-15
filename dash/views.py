```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        context = {
            'accounts': accounts,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm()
        }
        return render(request, 'account_management.html', context)

    elif request.method == 'POST':
        if 'add_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                messages.success(request, 'Account created successfully.')
                return redirect('account_management')
            else:
                messages.error(request, 'There was an error creating your account.')

        elif 'create_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                messages.success(request, 'Transaction completed successfully.')
                return redirect('account_management')
            else:
                messages.error(request, 'Transaction creation failed. Please check your details.')
    
    return JsonResponse({'status': 'Invalid request'}, status=400)
```