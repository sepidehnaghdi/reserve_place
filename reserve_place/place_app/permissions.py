from rest_framework import permissions
from django.contrib.auth.models import User, Group

from place_app.models import Rent


class PlacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif view.action == 'create':
            return request.user and request.user.is_superuser

        else:
            user_groups = request.user.groups.values_list('name', flat=True)
            return ("locator" in user_groups) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            user_groups = request.user.groups.values_list('name', flat=True)
            return ("locator" in user_groups and obj.user == request.user) or request.user.is_superuser


class RentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['POST', 'DELETE']:
            return "renter" in user_groups

        return False

    def has_object_permission(self, request, view, obj):
        user_groups = request.user.groups.values_list('name', flat=True)

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return "renter" in user_groups and obj.renter == request.user

        return False


class RenterCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['POST', 'PUT', 'PATCH']:
            return "renter" in user_groups

        if request.method == 'DELETE':
            return 'renter' in user_groups or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        user_groups = request.user.groups.values_list('name', flat=True)
        rent = Rent.objects.filter(renter=obj.renter, place=obj.place, status='r')

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH']:
            return "renter" in user_groups and rent.exists()

        if request.method == 'DELETE':
            return ('renter' in user_groups and rent.exists()) or request.user.is_superuser


class PlaceImagePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)

        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            return ("locator" in user_groups) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            user_groups = request.user.groups.values_list('name', flat=True)
            return ("locator" in user_groups and obj.place.user == request.user) or request.user.is_superuser
