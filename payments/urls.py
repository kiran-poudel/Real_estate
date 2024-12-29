from django.contrib import admin
from django.urls import path
from .views import create_payment,create_invoice,generate_receipt


urlpatterns = [
    path('payments/<int:properties_id>/',create_payment),
    path('invoice/<int:properties_id>/',create_invoice),
    path('receipt/<int:payment_id>/<int:invoice_id>/',generate_receipt),
]

