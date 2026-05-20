from rest_framework import permissions


class IsAuthenticatedAndAdminCanDelete(permissions.BasePermission):
    """
    Allows full CRUD to authenticated users, but restricts DELETE requests to staff members only.
    """

    def has_permission(self, request, view):
        """
        Checks if the request should be permitted.

        :param request: The incoming HTTP request.
        :param view: The view handling the request.
        :return: Boolean indicating permission status.
        """
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method == 'DELETE':
            return request.user.is_staff

        return True
