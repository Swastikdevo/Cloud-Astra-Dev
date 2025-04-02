```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

class AccountView(View):
    def get(self, request):
        accounts = Account.objects.all()
        return render(request, 'bank/accounts.html', {'accounts': accounts})

    def post(self, request):
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_list')
        return render(request, 'bank/accounts.html', {'form': form})

class TransactionView(View):
    def get(self, request):
        transactions = Transaction.objects.all()
        return render(request, 'bank/transactions.html', {'transactions': transactions})

    @csrf_exempt
    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'}, status=201)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    return render(request, 'bank/account_detail.html', {'account': account})

def deposit(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == "POST":
        amount = request.POST.get('amount')
        account.balance += float(amount)
        account.save()
        return redirect('account_detail', account_id=account.id)
    return render(request, 'bank/deposit.html', {'account': account})

def withdraw(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == "POST":
        amount = request.POST.get('amount')
        if account.balance >= float(amount):
            account.balance -= float(amount)
            account.save()
            return redirect('account_detail', account_id=account.id)
        return render(request, 'bank/withdraw.html', {'account': account, 'error': 'Insufficient funds'})
    return render(request, 'bank/withdraw.html', {'account': account})
```