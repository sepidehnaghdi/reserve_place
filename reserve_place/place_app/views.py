from django.shortcuts import render
from .models import Place, Rent
from rest_framework import viewsets
from .serializers import PlaceSerializer, RentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import PlacePermission, RentPermission


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (IsAuthenticated, PlacePermission)


class RentViewSet(viewsets.ModelViewSet):
    serializer_class = RentSerializer
    permission_classes = (IsAuthenticated, RentPermission)

    def get_queryset(self):
        queryset = Rent.objects.all()
        user_groups = self.request.user.groups.values_list('name', flat=True)

        if 'renter' in user_groups:
            queryset = queryset.filter(renter_id=self.request.user.id)

        if 'locator' in user_groups:
            queryset = queryset.filter(place__user=self.request.user)

        return queryset
