```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankAccount
from .forms import BankAccountForm

@login_required
def manage_account(request):
    try:
        user_account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        user_account = None

    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=user_account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account details updated successfully.')
            return redirect('manage_account')
        else:
            messages.error(request, 'Error updating account details. Please check the form.')

    else:
        form = BankAccountForm(instance=user_account)

    return render(request, 'bank/manage_account.html', {'form': form, 'account': user_account})
```