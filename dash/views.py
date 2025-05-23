```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import CreateAccountForm, FundAccountForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully'})
        
        elif 'fund_account' in request.POST:
            form = FundAccountForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'message': 'Account funded successfully'})

    else:
        accounts = Account.objects.filter(user=request.user)
        create_account_form = CreateAccountForm()
        fund_account_form = FundAccountForm()

    return render(request, 'manage_account.html', {
        'accounts': accounts,
        'create_account_form': create_account_form,
        'fund_account_form': fund_account_form
    })
```