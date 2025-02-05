```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import TransferForm
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required, name='dispatch')
class BankView(View):
    
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/home.html', {'accounts': accounts})

    @csrf_exempt
    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            receiver = form.cleaned_data['receiver']
            amount = form.cleaned_data['amount']
            
            if sender.balance >= amount:
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()

                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    user=request.user
                )
                return JsonResponse({'status': 'success', 'message': 'Transfer successful!'})

            return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
        return JsonResponse({'status': 'error', 'message': 'Invalid form submission.'})
```