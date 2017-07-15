from django.db import transaction
from django.shortcuts import render, get_object_or_404
from .models import Place, Rent, RenterComment, PlaceImage
from rest_framework import viewsets
from .serializers import PlaceSerializer, RentSerializer, RenterCommentSerializer, PlaceImageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import PlacePermission, RentPermission, RenterCommentPermission, PlaceImagePermission
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.parsers import MultiPartParser
from .filters import PlaceFilter


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (IsAuthenticated, PlacePermission)
    # filter_fields = ('user__first_name', 'user__last_name', 'province', 'city', 'address', 'place_type', 'start_rental_period', 'end_rental_period')
    filter_class = PlaceFilter


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


class RenterCommentViewSet(viewsets.ModelViewSet):
    queryset = RenterComment.objects.all()
    serializer_class = RenterCommentSerializer
    permission_classes = (IsAuthenticated, RenterCommentPermission)


class PlaceImageViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = PlaceImage.objects.all()
    parser_classes = (MultiPartParser,)
    serializer_class = PlaceImageSerializer
    permission_classes = (IsAuthenticated, PlaceImagePermission)
    http_method_names = ('get', 'post', 'delete')

    def perform_create(self, serializer):
        place = get_object_or_404(Place, id=self.kwargs['parent_lookup_place'])
        serializer.save(place=place, image_name=self.request.FILES['image'].name)

