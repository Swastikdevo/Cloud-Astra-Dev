from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Borrower, Activity
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from datetime import date

@login_required
def members(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_account = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']

            if account.balance >= amount:
                # Process the transfer
                account.balance -= amount
                recipient_account.balance += amount
                account.save()
                recipient_account.save()

                Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
                Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer', sender=account)

                return redirect('account_overview')

    else:
        form = TransferForm()

    context = {
        'account': account,
        'transactions': transactions,
        'form': form,
    }
    return render(request, 'bank/account_overview.html', context)

@require_POST
@login_required
def deposit(request):
    amount = request.POST.get('amount')
    account = Account.objects.get(user=request.user)
    account.balance += float(amount)
    account.save()

    Transaction.objects.create(account=account, amount=float(amount), transaction_type='Deposit')

    return JsonResponse({'success': True, 'new_balance': account.balance})

@require_POST
@login_required
def withdraw(request):
    amount = request.POST.get('amount')
    account = Account.objects.get(user=request.user)

    if account.balance >= float(amount):
        account.balance -= float(amount)
        account.save()

        Transaction.objects.create(account=account, amount=-float(amount), transaction_type='Withdrawal')

        return JsonResponse({'success': True, 'new_balance': account.balance})
    else:
        return JsonResponse({'success': False, 'error': 'Insufficient funds'})

@login_required
def members(request):
    """Main dashboard showing borrowers"""
    borrowers = Borrower.objects.all().order_by('-created_at')
    paginator = Paginator(borrowers, 10)  # Show 10 borrowers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'borrowers': page_obj,
        'total_borrowers': borrowers.count(),
    }
    return render(request, 'dash/members.html', context)

@csrf_exempt
def webhook(request):
    """Handle webhook requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process webhook data here
            return JsonResponse({'status': 'success', 'message': 'Webhook processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)

@login_required
def stats(request):
    """Display statistics dashboard"""
    total_borrowers = Borrower.objects.count()
    total_loan_amount = sum(b.loan_amount for b in Borrower.objects.all())
    overdue_borrowers = sum(1 for b in Borrower.objects.all() if b.days_left() == "Overdue")
    paid_borrowers = Borrower.objects.filter(payment_completed=True).count()
    
    context = {
        'total_borrowers': total_borrowers,
        'total_loan_amount': total_loan_amount,
        'overdue_borrowers': overdue_borrowers,
        'paid_borrowers': paid_borrowers,
    }
    return render(request, 'dash/stats.html', context)

@csrf_exempt
def ivr_response(request):
    """Handle IVR responses"""
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        response = request.POST.get('response')
        
        try:
            borrower = Borrower.objects.get(phone_number=phone_number)
            borrower.ivr_sent = True
            borrower.save()
            
            return JsonResponse({'status': 'success', 'message': 'IVR response recorded'})
        except Borrower.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Borrower not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)

@login_required
@require_POST
def process_input(request):
    """Process form input for creating/updating borrowers"""
    name = request.POST.get('name')
    phone_number = request.POST.get('phone_number')
    education = request.POST.get('education')
    loan_amount = request.POST.get('loan_amount')
    repayment_date = request.POST.get('repayment_date')
    cibil_score = request.POST.get('cibil_score')
    address = request.POST.get('address', '')
    email = request.POST.get('email', '')
    
    try:
        # Check if borrower already exists
        borrower, created = Borrower.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                'name': name,
                'education': education,
                'loan_amount': float(loan_amount) if loan_amount else 0,
                'repayment_last_date': repayment_date if repayment_date else date.today(),
                'cibil_score': int(cibil_score) if cibil_score else 750,
                'address': address,
                'email': email,
            }
        )
        
        if created:
            message = 'Borrower created successfully'
        else:
            # Update existing borrower
            borrower.name = name
            borrower.education = education
            borrower.loan_amount = float(loan_amount) if loan_amount else borrower.loan_amount
            borrower.repayment_last_date = repayment_date if repayment_date else borrower.repayment_last_date
            borrower.cibil_score = int(cibil_score) if cibil_score else borrower.cibil_score
            borrower.address = address
            borrower.email = email
            borrower.save()
            message = 'Borrower updated successfully'
        
        return JsonResponse({'status': 'success', 'message': message})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# Additional utility views for the dashboard

@login_required
def borrower_detail(request, borrower_id):
    """View details of a specific borrower"""
    try:
        borrower = Borrower.objects.get(id=borrower_id)
        context = {'borrower': borrower}
        return render(request, 'dash/borrower_detail.html', context)
    except Borrower.DoesNotExist:
        return JsonResponse({'error': 'Borrower not found'}, status=404)

@login_required
@require_POST
def mark_payment_complete(request, borrower_id):
    """Mark a borrower's payment as complete"""
    try:
        borrower = Borrower.objects.get(id=borrower_id)
        borrower.payment_completed = True
        borrower.payment_date = date.today()
        borrower.save()
        
        return JsonResponse({'status': 'success', 'message': 'Payment marked as complete'})
    except Borrower.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Borrower not found'}, status=404)
```