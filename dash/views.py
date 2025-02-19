```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_management_view(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    context = {'accounts': accounts}

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                deposit_form.save(user)
                return redirect('bank_management')
        
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                withdrawal_form.save(user)
                return redirect('bank_management')
        
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                transfer_form.save(user)
                return redirect('bank_management')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    context.update({
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })

    return render(request, 'bank_management.html', context)

def ajax_account_balance(request):
    if request.is_ajax() and request.method == "GET":
        account_id = request.GET.get('account_id')
        account = Account.objects.get(id=account_id)
        return JsonResponse({'balance': account.balance})
    return JsonResponse({'error': 'Invalid request'}, status=400)
```