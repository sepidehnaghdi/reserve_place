from rest_framework import permissions
from django.contrib.auth.models import User, Group


class PlacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True

        elif view.action == 'create':
            return request.user and request.user.is_superuser

        else:
            user_groups = request.user.groups.values_list('name', flat=True)
            return ("locator" in user_groups) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        else:
            user_groups = request.user.groups.values_list('name', flat=True)
            return ("locator" in user_groups and obj.user == request.user) or request.user.is_superuser

