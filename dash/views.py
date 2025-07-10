```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import TransferForm

@method_decorator(login_required, name='dispatch')
class BankView(View):
    template_name = 'bank/home.html'

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, self.template_name, {'accounts': accounts})

    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account = form.cleaned_data['sender_account']
            receiver_account = form.cleaned_data['receiver_account']
            amount = form.cleaned_data['amount']

            # Transfer logic
            if sender_account.balance >= amount:
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()

                # Log transaction
                Transaction.objects.create(
                    sender=sender_account,
                    receiver=receiver_account,
                    amount=amount,
                    user=request.user
                )

                return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid data.'})
```