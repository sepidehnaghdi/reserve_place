from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import JSONField


class Place(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    PROVINCE_CHOICES = (
        ('isf', 'Isfahan'),
        ('teh', 'Tehran'),
        ('shr', 'shiraz')
    )
    province = models.CharField(choices=PROVINCE_CHOICES, null=False, blank=False, max_length=100)
    city = models.CharField(null=False, blank=False, max_length=100)
    address = models.TextField(null=False, blank=False)
    year_of_construction = models.PositiveIntegerField(null=False, blank=False)
    PLACE_TYPE_CHOICES = (
        ('v', 'villa'),
        ('g', 'garden'),
        ('h', 'house'),
        ('s', 'suite'),
        ('o', 'other')
    )

    place_type = models.CharField(null=False, blank=False, choices=PLACE_TYPE_CHOICES, max_length=1)
    home_document_file = models.FileField(blank=False, null=False, upload_to="home_document_file")  # تصویر سند ملک

    total_area = models.BigIntegerField(null=False, blank=False)# m2
    construction_area = models.BigIntegerField(null=False, blank=False)# m2
    num_of_bed_rooms = models.BigIntegerField(null=False, blank=False)
    max_num_of_people = models.PositiveIntegerField(null=False, blank=False)
    allowed_more_people = models.BooleanField(null=False, blank=False)
    allowed_pet = models.BooleanField(null=False, blank=False)
    start_rental_period = models.DateField(null=True, blank=True)
    end_rental_period = models.DateField(null=True, blank=True)
    price_per_night = models.BigIntegerField(null=True, blank=True)
    assignment_time = models.TimeField(null=True, blank=True) #ساعت واگذاری
    delivery_time = models.TimeField(null=True, blank=True) # ساعت تحویل
    price_for_each_more_person = models.BigIntegerField(null=True, blank=True)
    rental_conditions = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    services = JSONField(null=True, blank=True)
    surroundings = models.TextField(null=True, blank=True)
    distance_from_store = models.BigIntegerField(null=True, blank=True)
    distance_from_restaurant = models.BigIntegerField(null=True, blank=True)



