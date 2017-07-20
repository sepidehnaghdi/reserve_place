from django.db import transaction
from django.shortcuts import render, get_object_or_404
from .models import Place, Rent, RenterComment, PlaceImage
from rest_framework import viewsets
from .serializers import PlaceSerializer, RentSerializer, RenterCommentSerializer, PlaceImageSerializer, \
    UpdatePlaceByLocatorSerializer, GetCommentByLocatorSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import PlacePermission, RentPermission, RenterCommentPermission, PlaceImagePermission
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.parsers import MultiPartParser
from .filters import PlaceFilter
from rest_framework.exceptions import PermissionDenied


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticated, PlacePermission)
    filter_class = PlaceFilter


    def get_serializer_class(self):
        user_groups = self.request.user.groups.values_list('name', flat=True)
        if self.request.method in ['PUT', 'PATCH'] and "locator" in user_groups:
            return UpdatePlaceByLocatorSerializer
        else:
            return PlaceSerializer

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

        place = self.request.query_params.get('place', None)
        if place:
            queryset = queryset.filter(place_id=place)

        return queryset


class RenterCommentViewSet(viewsets.ModelViewSet):
    queryset = RenterComment.objects.all()
    permission_classes = (IsAuthenticated, RenterCommentPermission)

    def get_serializer_class(self):
        user_groups = self.request.user.groups.values_list('name', flat=True)
        if self.request.method == 'GET' and 'locator' in user_groups:
            return GetCommentByLocatorSerializer
        else:
            return RenterCommentSerializer

    def get_queryset(self):
        queryset = RenterComment.objects.all()
        queryset = queryset.filter(place=self.kwargs['parent_lookup_place'])
        return queryset


class PlaceImageViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,)
    serializer_class = PlaceImageSerializer
    permission_classes = (IsAuthenticated, PlaceImagePermission)
    http_method_names = ('get', 'post', 'delete')

    def get_queryset(self):
        queryset = PlaceImage.objects.all()

        place = get_object_or_404(Place, id=self.kwargs['parent_lookup_place'])
        queryset = queryset.filter(place=place)
        return queryset

    def perform_create(self, serializer):
        place = get_object_or_404(Place, id=self.kwargs['parent_lookup_place'])

        if place.user != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied

        serializer.save(place=place, image_name=self.request.FILES['image'].name)

