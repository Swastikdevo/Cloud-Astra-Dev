```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Account, Transaction
from .forms import TransferForm

@method_decorator(login_required, name='dispatch')
class BankView(View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/home.html', {'accounts': accounts})

    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = form.cleaned_data['sender_account']
            receiver_account = form.cleaned_data['receiver_account']
            amount = form.cleaned_data['amount']

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()

                # Log the transaction
                Transaction.objects.create(
                    sender=sender_account,
                    receiver=receiver_account,
                    amount=amount,
                )
                return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
        return JsonResponse({'status': 'error', 'message': 'Invalid form submission.'})

    def new_feature(self, request):
        # Example new feature: View Transactions
        transactions = Transaction.objects.filter(sender__user=request.user).order_by('-date')
        return render(request, 'bank/transactions.html', {'transactions': transactions})
```