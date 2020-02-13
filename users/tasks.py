from celery import shared_task
# from time import sleep
from django.core.mail import send_mail

#it was tesr for celety+redis
# @shared_task
# def sleepy(duration):
#   sleep(duration)


@shared_task
def send_email_task(sub, mess, sen, recip, fail_silently=True):
    send_mail(sub, mess, sen, recip, fail_silently=True)
