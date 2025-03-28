```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import TransactionForm, AccountForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        form = TransactionForm()
        return render(request, 'bank_management.html', {'accounts': accounts, 'form': form})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']

            if transaction_type == 'deposit':
                account.balance += amount
                account.save()
            elif transaction_type == 'withdraw' and account.balance >= amount:
                account.balance -= amount
                account.save()
            else:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)

            Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type=transaction_type
            )
            return JsonResponse({'message': 'Transaction completed successfully'})

        return JsonResponse({'error': 'Invalid form data'}, status=400)
    
    return redirect('bank_management_view')
```