```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account_view(request):
    user_accounts = Account.objects.filter(user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.user = request.user
            transaction.save()
            return JsonResponse({"message": "Transaction completed successfully!"}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    return render(request, 'accounts/manage_account.html', {'accounts': user_accounts})
```