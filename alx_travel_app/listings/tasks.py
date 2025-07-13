# listings/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(booking_id, user_email, listing_title):
    subject = 'Booking Confirmation'
    message = f"""
    Dear Customer,

    Your booking for {listing_title} has been confirmed!
    Booking ID: {booking_id}

    Thank you for using ALX Travel App!
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
