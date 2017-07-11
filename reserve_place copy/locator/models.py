from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.


class LocatorProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    contact_number = models.CharField(max_length=15, blank=True, null=True)
    Second_contact_number = models.CharField(max_length=15, blank=True, null=True)
    relative_contact_number = models.CharField(max_length=15, blank=True, null=True)

    image_of_national_card = models.FileField(blank=True, null=True, upload_to="national_cards")  # کارت ملی
    image_of_birth_certificate = models.FileField(blank=True, null=True, upload_to="birth_certificate")  # شناسنامه
    image_of_clearance = models.FileField(blank=True, null=True, upload_to="clearance")  # گواهی سو پیشینه

    birth_certificate_number = models.CharField(max_length=10, blank=True, null=True)  # شماره شناسنامه
    national_number = models.CharField(max_length=10, blank=True, null=True)  # شماره ملی
