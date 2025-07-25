```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@require_POST
@csrf_exempt
def create_account(request):
    account_holder = request.POST.get('account_holder')
    initial_balance = request.POST.get('initial_balance', 0)
    
    if account_holder:
        account = Account.objects.create(holder_name=account_holder, balance=initial_balance)
        return JsonResponse({'status': 'success', 'account_id': account.id}, status=201)
    return JsonResponse({'status': 'error', 'message': 'Account holder name is required'}, status=400)

@require_POST
@csrf_exempt
def deposit_funds(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        account_id = form.cleaned_data['account_id']
        amount = form.cleaned_data['amount']
        
        try:
            account = Account.objects.get(id=account_id)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        except Account.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid input'}, status=400)

@require_POST
@csrf_exempt
def withdraw_funds(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        account_id = form.cleaned_data['account_id']
        amount = form.cleaned_data['amount']
        
        try:
            account = Account.objects.get(id=account_id)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'}, status=400)
        except Account.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid input'}, status=400)

def account_details(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        transactions = Transaction.objects.filter(account=account).order_by('-created_at')
        return render(request, 'account/details.html', {'account': account, 'transactions': transactions})
    except Account.DoesNotExist:
        return render(request, 'account/not_found.html', {'error': 'Account not found'})
```