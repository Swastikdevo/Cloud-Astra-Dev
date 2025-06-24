```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@csrf_exempt
def manage_account_view(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.save()
            return JsonResponse({'success': True, 'message': 'Transaction completed successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'bank/manage_account.html', {'accounts': accounts})
```