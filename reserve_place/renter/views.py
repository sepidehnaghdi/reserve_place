from django.shortcuts import render
from rest_framework import viewsets
from .models import RenterProfile
from .serializers import RenterProfileSerializer
from .permissions import RenterPermission

class RenterProfileViewSet(viewsets.ModelViewSet):
    queryset = RenterProfile.objects.all()
    serializer_class = RenterProfileSerializer
    permission_classes = (RenterPermission, )
    http_method_names = ('get', 'put', 'patch')
