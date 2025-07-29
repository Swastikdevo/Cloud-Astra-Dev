```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_POST
@csrf_exempt
def manage_account(request):
    if request.method == "POST":
        action_type = request.POST.get('action')
        
        if action_type == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({"success": True, "new_balance": account.balance})

        elif action_type == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
                    return JsonResponse({"success": True, "new_balance": account.balance})
                else:
                    return JsonResponse({"success": False, "error": "Insufficient funds."})
            
        return JsonResponse({"success": False, "error": "Invalid action."})
    
    return render(request, 'account/manage_account.html')
```