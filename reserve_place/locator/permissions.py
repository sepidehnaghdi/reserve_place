from rest_framework import permissions
from django.contrib.auth.models import User, Group

class LocatorPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if view.action == 'list':
            return request.user and request.user.is_superuser

        elif view.action in ['post', 'delete']:
            return False

        else:
            user_groups = request.user.groups.values_list('name', flat=True)
            return ("locator" in user_groups) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
            user_groups = request.user.groups.values_list('name', flat=True)
            return ("locator" in user_groups and obj.user == request.user) or request.user.is_superuser

