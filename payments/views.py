from django.shortcuts import render, redirect
from .models import properties, Payment, Invoice, Receipt
from .Forms import PaymentForm, InvoiceForm
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from django.contrib.auth import get_user_model
User= get_user_model()
from rest_framework.decorators import api_view,permission_classes
from properties.models import properties
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAdminUser,IsAuthenticated])
def create_payment(request, properties_id):
    property = properties.objects.get(id=properties_id)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.property = property
            payment.save()
            return JsonResponse({
                "message": "Payment created successfully",
                "payment_id": payment.id,
                "property_id": property.id,
                "amount": payment.amount,
            }, status=201)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": "GET method not allowed. Use POST."}, status=405)

@api_view(['POST'])
@permission_classes([IsAdminUser,IsAuthenticated])
def create_invoice(request, properties_id):
    property = properties.objects.get(id=properties_id)
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.property = property
            invoice.save()
            return JsonResponse({
                "message": "Invoice created successfully",
                "invoice_id": invoice.id,
                "property_id": property.id,
                "total_amount": invoice.total_amount,
                "payment_due_date": invoice.payment_due_date,
            }, status=201)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": "GET method not allowed. Use POST."}, status=405)


@api_view(['get'])
@permission_classes([IsAdminUser,IsAuthenticated])
def generate_receipt(request, payment_id,invoice_id):
    # Fetch the Payment object using the provided payment_id
    payment = get_object_or_404(Payment, id=payment_id)
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Create a receipt for the payment
    receipt = Receipt.objects.create(payment=payment, receipt_number=f"REC-{payment.id}",invoice= invoice)
    
    # Return a JSON response with receipt details
    return JsonResponse({
        "message": "Receipt generated successfully",
        "receipt_number": receipt.receipt_number,
        "payment_id": payment.id,
        "amount":payment.amount,
        "invoice_id":invoice.id,
        "customer_name":invoice.customer_name,
        "total_amount":invoice.total_amount,
    }, status=201)

