```python
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
import json

@method_decorator(csrf_exempt, name='dispatch')
class BankAccountView(LoginRequiredMixin, View):

    def get(self, request, account_id=None):
        if account_id:
            # Fetch account details
            account = self.get_account_details(account_id)
            return JsonResponse(account)
        else:
            # Fetch all accounts for the user
            accounts = self.get_all_accounts_for_user(request.user)
            return JsonResponse(accounts, safe=False)

    def post(self, request):
        # Create a new bank account
        data = json.loads(request.body)
        account = self.create_account(data, request.user)
        return JsonResponse(account, status=201)

    def put(self, request, account_id):
        # Update existing account details
        data = json.loads(request.body)
        updated_account = self.update_account(account_id, data)
        return JsonResponse(updated_account)

    def delete(self, request, account_id):
        # Close an existing account
        self.close_account(account_id)
        return JsonResponse({'message': 'Account closed successfully.'}, status=204)

    def get_account_details(self, account_id):
        # Logic to fetch account details from the database
        pass

    def get_all_accounts_for_user(self, user):
        # Logic to fetch all accounts for the authenticated user from the database
        pass

    def create_account(self, data, user):
        # Logic to create a new account based on the provided data
        pass

    def update_account(self, account_id, data):
        # Logic to update the account with the provided account_id and data
        pass

    def close_account(self, account_id):
        # Logic to close the account with the provided account_id
        pass
```