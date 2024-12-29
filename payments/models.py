from django.db import models
from properties.models import properties
from django.utils import timezone

# Create your models here.

class Payment(models.Model):
    class PaymentType(models.TextChoices):
       CASH = 'Cash',
       BANKTRANSFER = 'BankTransfer',
       CHEQUE = 'Cheque',
    
    property = models.ForeignKey(properties, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50, choices=PaymentType.choices,default = PaymentType.CASH)

    def __str__(self):
        return f"Payment of {self.amount} for {self.property.title}"

class Invoice(models.Model):
    property = models.ForeignKey(properties, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    issue_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_date = models.DateTimeField()

    def __str__(self):
        return f"Invoice for {self.customer_name} - {self.property.title}"

class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=50, unique=True)
    receipt_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Receipt for {self.payment.amount} - {self.receipt_number}"