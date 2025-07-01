```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from .forms import TransactionForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = BankAccount.objects.filter(user=request.user)
        return render(request, 'manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction completed'})
        return JsonResponse({'status': 'error', 'message': 'Invalid form data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
```