from django.contrib import admin
from .models import Payment,Invoice,Receipt

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'amount', 'payment_method',)
    list_display_links=('id','property','amount','payment_method',)
    search_fields=('property','amount',)
    list_per_page = 25

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name','total_amount',)
    list_display_links=('id', 'customer_name','total_amount',)
    list_per_page = 25
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'receipt_number','payment',)
    list_display_links=('id','receipt_number','payment',)
    list_per_page = 25

admin.site.register(Payment,PaymentAdmin)
admin.site.register(Invoice,InvoiceAdmin)
admin.site.register(Receipt,ReceiptAdmin)

