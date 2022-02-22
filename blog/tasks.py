from celery import shared_task

from django.core.mail import send_mail

from Practice.celery import app


@shared_task()
def contact_us(email, text):
    send_mail(
        'support',
        {text},
        [{email}],
        'from@example.com',
        fail_silently=False,
    )
