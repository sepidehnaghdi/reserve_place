from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.exceptions import ValidationError


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

    total_area = models.BigIntegerField(null=False, blank=False)  # m2
    construction_area = models.BigIntegerField(null=False, blank=False)  # m2
    num_of_bed_rooms = models.BigIntegerField(null=False, blank=False)
    max_num_of_people = models.PositiveIntegerField(null=False, blank=False)
    allowed_more_people = models.BooleanField(null=False, blank=False)
    allowed_pet = models.BooleanField(null=False, blank=False)
    start_rental_period = models.DateField(null=True, blank=True)
    end_rental_period = models.DateField(null=True, blank=True)
    price_per_night = models.BigIntegerField(null=True, blank=True)
    assignment_time = models.TimeField(null=True, blank=True)  # ساعت واگذاری
    delivery_time = models.TimeField(null=True, blank=True)  # ساعت تحویل
    price_for_each_more_person = models.BigIntegerField(null=True, blank=True)
    rental_conditions = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    services = JSONField(null=True, blank=True)
    surroundings = models.TextField(null=True, blank=True)
    distance_from_store = models.BigIntegerField(null=True, blank=True)
    distance_from_restaurant = models.BigIntegerField(null=True, blank=True)


class Rent(models.Model):
    renter = models.ForeignKey(User, null=False, blank=False)
    place = models.ForeignKey(Place, null=False, blank=False)
    check_in_date = models.DateField(null=False, blank=False)
    check_out_date = models.DateField(null=False, blank=False)
    STATUS_CHOICES = (
        ('t', 'temporarily_reserved'),
        ('r', 'reserved')
    )
    status = models.CharField(choices=STATUS_CHOICES, null=False, blank=False, max_length=1, default='t')
    updated = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        rents = Rent.objects.filter(place=self.place, status='r')
        if rents.exists():
            for rent in rents:
                if (rent.check_out_date >= self.check_in_date and rent.check_out_date <= self.check_out_date) or \
                        (rent.check_in_date >= self.check_in_date and rent.check_in_date <= self.check_out_date):
                    raise ValidationError("someone reserve this place in this period before.")

        if (str(self.check_in_date) < str(self.place.start_rental_period) or
                    str(self.check_out_date) > str(self.place.end_rental_period)):
            raise ValidationError('you cannot rent this place in this period')

        super(Rent, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.status == 'r':
            raise ValidationError('cannot delete and cancel reserved place')

        super(Rent, self).delete()


class RenterComment(models.Model):
    renter = models.ForeignKey(User, null=False, blank=False)
    place = models.ForeignKey(Place, null=False, blank=False)
    facilities_score = models.PositiveIntegerField(null=False, blank=False,
                                                   validators=[MaxValueValidator(5), MinValueValidator(1)])
    cleanness_score = models.PositiveIntegerField(null=False, blank=False,
                                                  validators=[MaxValueValidator(5), MinValueValidator(1)])
    surroundings_score = models.PositiveIntegerField(null=False, blank=False,
                                                     validators=[MaxValueValidator(5), MinValueValidator(1)])
    price_achievement_score = models.PositiveIntegerField(null=False, blank=False,
                                                          validators=[MaxValueValidator(5), MinValueValidator(1)])
    locator_score = models.PositiveIntegerField(null=False, blank=False,
                                                validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(null=True, blank=True)


class PlaceImage(models.Model):
    place = models.ForeignKey(Place, null=False, blank=False)
    image = models.FileField(null=False, blank=False, upload_to="image_file")
    description = models.TextField(null=True, blank=True)
    image_name = models.CharField(max_length=255, blank=True, null=False)
