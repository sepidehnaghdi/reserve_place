from django.shortcuts import render
from rest_framework import viewsets
from .models import LocatorProfile
from .serializers import LocatorProfileSerializer
from .permissions import LocatorPermission

class LocatorProfileViewSet(viewsets.ModelViewSet):
    queryset = LocatorProfile.objects.all()
    serializer_class = LocatorProfileSerializer
    permission_classes = (LocatorPermission, )
    http_method_names = ('get', 'put', 'patch')
