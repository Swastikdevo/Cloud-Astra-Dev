```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction, UserProfile
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account/manage.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'success': True, 'message': 'Account created successfully!'})
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@csrf_exempt
def transfer_funds(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            sender_account = form.cleaned_data['sender_account']
            receiver_account = form.cleaned_data['receiver_account']
            amount = form.cleaned_data['amount']

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()

                transaction = Transaction(sender=sender_account, receiver=receiver_account, amount=amount)
                transaction.save()
                return JsonResponse({'success': True, 'message': 'Transfer successful!'})
            else:
                return JsonResponse({'success': False, 'message': 'Insufficient balance!'})

        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
```