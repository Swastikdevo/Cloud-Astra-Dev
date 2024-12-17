```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import BankAccount
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    account = BankAccount.objects.get(user=request.user)

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                return JsonResponse({'success': True, 'new_balance': account.balance}, status=200)

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    return JsonResponse({'success': True, 'new_balance': account.balance}, status=200)
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    return render(request, 'account_management.html', context)
```