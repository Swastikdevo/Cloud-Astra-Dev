```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account
from .forms import AccountForm
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account_management.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

    elif request.method == 'DELETE':
        account_id = request.POST.get('account_id')
        try:
            account = Account.objects.get(id=account_id, user=request.user)
            account.delete()
            return JsonResponse({'message': 'Account deleted successfully!'}, status=204)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found!'}, status=404)

    return JsonResponse({'error': 'Method not allowed!'}, status=405)
```