from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if view.action == 'list':
            return request.user and request.user.is_superuser

        elif view.action == 'retrieve':
            return True

        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user and request.user.is_superuser
        else:
            return request.user and (request.user.is_superuser or request.user == obj)
