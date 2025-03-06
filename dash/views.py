```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm

@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            if account_id:
                account = get_object_or_404(Account, id=account_id)
                for attr, value in form.cleaned_data.items():
                    setattr(account, attr, value)
                account.save()
                return JsonResponse({'message': 'Account updated successfully!'})
            else:
                new_account = form.save()
                return JsonResponse({'message': 'Account created successfully!', 'account_id': new_account.id})
        return JsonResponse({'errors': form.errors}, status=400)

    elif request.method == "GET":
        if account_id:
            account = get_object_or_404(Account, id=account_id)
            return render(request, 'accounts/account_detail.html', {'account': account})
        else:
            accounts = Account.objects.all()
            return render(request, 'accounts/account_list.html', {'accounts': accounts})

@csrf_exempt
@require_http_methods(["POST"])
def transfer_funds(request):
    data = request.POST
    try:
        from_account = get_object_or_404(Account, id=data['from_account_id'])
        to_account = get_object_or_404(Account, id=data['to_account_id'])
        amount = float(data['amount'])

        if from_account.balance < amount:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)

        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()

        Transaction.objects.create(from_account=from_account, to_account=to_account, amount=amount)

        return JsonResponse({'message': 'Transfer successful!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```