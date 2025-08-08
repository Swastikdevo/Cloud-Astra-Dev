```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from django.contrib import messages

@login_required
@require_http_methods(["POST", "GET"])
def account_management(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        account_id = request.POST.get('account_id')
        amount = float(request.POST.get('amount', 0))

        try:
            account = Account.objects.get(id=account_id, user=request.user)

            if action == 'deposit':
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, f'Deposited ${amount} successfully!')

            elif action == 'withdraw':
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    messages.success(request, f'Withdrew ${amount} successfully!')
                else:
                    messages.error(request, 'Insufficient funds for this withdrawal.')

            elif action == 'transfer':
                recipient_id = request.POST.get('recipient_id')
                recipient_account = Account.objects.get(id=recipient_id)
                if account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='transfer', recipient=recipient_account)
                    messages.success(request, f'Transferred ${amount} to {recipient_account.user.username} successfully!')
                else:
                    messages.error(request, 'Insufficient funds for this transfer.')

        except Account.DoesNotExist:
            messages.error(request, 'Account not found.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

        return redirect('account_management')

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'account_management.html', {'accounts': accounts})
```