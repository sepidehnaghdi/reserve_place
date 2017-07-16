import hashlib
from random import random

from django.shortcuts import render
from django.core.mail import send_mail


# Create your views here.
from rest_framework.status import HTTP_400_BAD_REQUEST


def generate_confirmation_key(user_email):
    """
    The confirmation key for the ``User`` will be a
    SHA1 hash, generated from a combination of the ``User``'s
    email and a random salt.
    """
    try:
        salt = hashlib.sha1(str(random()).encode('utf-8')).hexdigest()
        email = user_email
        confirmation_key = hashlib.sha1((salt + email).encode('utf-8')).hexdigest()
        return confirmation_key
    except Exception as e:
        raise HTTP_400_BAD_REQUEST

from django.conf import settings

def send_confirmation_email(user_email, confirmation_key):
    print("user_email:", user_email)
    try:
        send_mail(
            'Confirmation Email',
            'please click on below link to confirm your registration:'
            ' \n 127.0.0.1:8000/api/v1/confirm?confirmation_key=' + confirmation_key,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
    except Exception as e:
        print("an error during sending email", str(e))
        raise HTTP_400_BAD_REQUEST
