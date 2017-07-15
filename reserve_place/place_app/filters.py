from django.db import models as django_models
import django_filters
from rest_framework import filters
from rest_framework import viewsets
from .models import Place


class PlaceFilter(filters.FilterSet):
    class Meta:
        model = Place
        fields = {
            'start_rental_period': ('gte', ),
            'end_rental_period': ('lte', ),
            'user__first_name': ('exact', ),
            'user__last_name': ('exact', ),
            'province': ('exact', ),
            'city': ('exact', ),
            'address': ('contains', ),
            'place_type': ('exact', )

        }