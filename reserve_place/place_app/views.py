from django.shortcuts import render
from .models import Place
from rest_framework import viewsets
from .serializers import PlaceSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import PlacePermission

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (IsAuthenticated, PlacePermission)