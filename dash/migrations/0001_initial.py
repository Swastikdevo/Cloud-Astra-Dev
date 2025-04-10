# Generated by Django 5.1.3 on 2024-11-19 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Full name of the borrower', max_length=100)),
                ('phone_number', models.CharField(help_text='Contact number (unique)', max_length=15, unique=True)),
                ('education', models.CharField(help_text='Educational qualification', max_length=50)),
                ('loan_amount', models.DecimalField(decimal_places=2, help_text='Loan amount in INR', max_digits=10)),
                ('repayment_last_date', models.DateField(help_text='Last repayment date')),
                ('cibil_score', models.PositiveIntegerField(help_text='CIBIL score of the borrower (range: 300 to 900)')),
                ('address', models.TextField(blank=True, help_text="Borrower's address")),
                ('email', models.EmailField(blank=True, help_text='Optional email address', max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
