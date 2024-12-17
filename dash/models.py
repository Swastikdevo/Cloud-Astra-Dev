from django.db import models
from datetime import date

class Borrower(models.Model):
    # Borrower's personal information
    name = models.CharField(max_length=100, help_text="Full name of the borrower")
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        help_text="Contact number (unique)"
    )
    education = models.CharField(max_length=50, help_text="Educational qualification")

    # Loan details
    loan_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Loan amount in INR"
    )
    repayment_last_date = models.DateField(help_text="Last repayment date")
    cibil_score = models.PositiveIntegerField(
        help_text="CIBIL score of the borrower (range: 300 to 900)"
    )

    # Additional fields
    address = models.TextField(blank=True, help_text="Borrower's address")
    email = models.EmailField(blank=True, help_text="Optional email address")
    message_sent = models.BooleanField(default=False)
    ivr_sent = models.BooleanField(default=False)
    whatsapp_sent = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    
    # Payment status
    payment_completed = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    notification_attempts = models.IntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"
    def days_left(self):
        today = date.today()
        return (self.repayment_last_date - today).days if self.repayment_last_date >= today else "Overdue"

class Activity(models.Model):
    date = models.DateField()
    name = models.TextField(blank=True, help_text="Name of Subject")
    hours_spent = models.FloatField()  # Hours spent on the activity
    
    def __str__(self):
        return f"{self.date}: {self.hours_spent} hours"