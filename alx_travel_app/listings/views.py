import os
import requests
from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from celery import shared_task
from django.core.mail import send_mail
from .tasks import send_booking_confirmation_email


# Temporary start
from django.http import HttpResponse
from django.conf import settings

def test_chapa_key(request):
    return HttpResponse(f"Chapa Key: {settings.CHAPA_SECRET_KEY}")
# Temporary end


# Create your views here.
class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed or edited.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all listings",
        responses={200: ListingSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new listing",
        request_body=ListingSerializer,
        responses={201: ListingSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all bookings",
        responses={200: BookingSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new booking",
        request_body=BookingSerializer,
        responses={201: BookingSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        booking = serializer.save()
        # Trigger the Celery task to send the confirmation email
        send_booking_confirmation_email.delay(
            booking.id,
            booking.user.email,
            booking.listing.title
        )


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get('booking_id')
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare Chapa API request
        chapa_url = 'https://api.chapa.co/v1/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'amount': str(booking.total_price),
            'currency': 'ETB',
            'email': request.user.email,
            'tx_ref': f'chapa-tx-{booking.id}-{request.user.id}',
            'callback_url': 'http://your-domain.com/api/payments/verify/',
            'return_url': 'http://your-domain.com/payment/success/',
        }

        try:
            response = requests.post(chapa_url, json=payload, headers=headers)
            response_data = response.json()

            if response_data.get('status') == 'success':
                # Create Payment record
                payment = Payment.objects.create(
                    booking=booking,
                    user=request.user,
                    amount=booking.total_price,
                    transaction_id=payload['tx_ref'],
                    status='PENDING'
                )
                return JsonResponse({
                    'message': 'Payment initiated successfully',
                    'payment_url': response_data['data']['checkout_url'],
                    'payment': PaymentSerializer(payment).data
                }, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Failed to initiate payment'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get('tx_ref')
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verify payment with Chapa
        chapa_url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(chapa_url, headers=headers)
            response_data = response.json()

            if response_data.get('status') == 'success':
                payment.status = 'COMPLETED'
                payment.save()
                # Trigger email confirmation
                send_payment_confirmation_email.delay(payment.id)        # Trigger email task
                return JsonResponse({
                    'message': 'Payment verified successfully',
                    'payment': PaymentSerializer(payment).data
                }, status=status.HTTP_200_OK)
            else:
                payment.status = 'FAILED'
                payment.save()
                return JsonResponse({'error': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            payment.status = 'FAILED'
            payment.save()
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@shared_task
def send_payment_confirmation_email(payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        subject = 'Payment Confirmation'
        message = f"""
        Dear {payment.user.get_full_name() or payment.user.username},
        
        Your payment of {payment.amount} ETB for booking #{payment.booking.id} has been successfully processed.
        Transaction ID: {payment.transaction_id}
        Status: {payment.status}
        
        Thank you for choosing our service!
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [payment.user.email],
            fail_silently=False,
        )
    except Payment.DoesNotExist:
        pass  # Log error if needed
