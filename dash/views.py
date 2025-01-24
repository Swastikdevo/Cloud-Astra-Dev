```python
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from django.views.decorators.csrf import csrf_exempt
import json

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AccountView(View):

    def get(self, request, account_id=None):
        if account_id:
            try:
                account = Account.objects.get(id=account_id, user=request.user)
                return JsonResponse(account.serialize(), safe=False)
            except Account.DoesNotExist:
                return JsonResponse({'error': 'Account not found'}, status=404)
        else:
            accounts = Account.objects.filter(user=request.user)
            return JsonResponse([account.serialize() for account in accounts], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        account = Account.objects.create(
            user=request.user,
            account_type=data.get('account_type'),
            balance=data.get('balance', 0),
        )
        return JsonResponse(account.serialize(), status=201)

    def put(self, request, account_id):
        data = json.loads(request.body)
        try:
            account = Account.objects.get(id=account_id, user=request.user)
            account.balance = data.get('balance', account.balance)
            account.save()
            return JsonResponse(account.serialize())
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)

    def delete(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id, user=request.user)
            account.delete()
            return JsonResponse({'message': 'Account deleted'}, status=204)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)
```