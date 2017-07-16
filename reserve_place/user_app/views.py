from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from user_app.serializers import RegisterSerializer, UserSerializer, GroupSerializer, DjangoGroupSerializer, ConfirmationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_app.permissions import IsSuperUser, UserPermission
from rest_framework import response, status
from django.db import transaction
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, \
    HTTP_400_BAD_REQUEST
from rest_framework_tracking.mixins import LoggingMixin
from .models import EmailConfirmation
import datetime
from locator.models import LocatorProfile
from renter.models import RenterProfile


class UserViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, UserPermission)
    http_method_names = ('get', 'put', 'patch', 'delete')
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class RegisterViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('post',)


class GroupViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = DjangoGroupSerializer
    permission_classes = (IsAuthenticated, IsSuperUser)


class ConfirmationViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = EmailConfirmation.objects.all()
    serializer_class = ConfirmationSerializer
    permission_classes = (AllowAny, )

    def list(self, request, *args, **kwargs):
        try:
            confirmation_key = self.request.query_params.get('confirmation_key')

            try:
                email_confirmation = EmailConfirmation.objects.get\
                    (confirmation_key=confirmation_key, expire_time__gt=datetime.datetime.now())
            except:
                from rest_framework.exceptions import NotFound
                raise NotFound

            user = User.objects.get(username=email_confirmation.user.username)
            user.is_active = True
            user.save()

        except Exception as e:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_200_OK)
