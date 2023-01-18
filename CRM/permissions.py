from rest_framework.permissions import BasePermission, SAFE_METHODS

from authentication.models import CRMUser


class IsRelatedOrReadOnly(BasePermission):
    """
    Object-level permission to only allow assignee of instance to edit it.
    """

    def has_object_permission(self, request, view, obj):
        """ Read permissions are allowed to any request,
        other permissions are allowed only to referenced author"""
        if request.method in SAFE_METHODS:
            return True

        if request.user.team == CRMUser.MANAGEMENT:
            return True

        return obj.is_related(request.user)
